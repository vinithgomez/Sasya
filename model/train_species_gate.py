#!/usr/bin/env python3
"""
Fine-tune MobileNetV3-Small (ImageNet pretrained) on data/species_gate/ for a
binary "is this photo one of our 7 supported crop species, or a different
species?" gate. This is a separate model from the 30-class disease
classifier (model/train.py / model/krishivision_model.pt) -- it runs before
that model, to catch out-of-scope species (e.g. a pear or apple leaf) before
they get confidently misclassified as one of the 30 trained disease classes.

This script is fully standalone: it does not import from, modify, or
otherwise touch model/train.py or model/krishivision_model.pt.

Expects data/species_gate/in_scope/ and data/species_gate/out_of_scope/,
built by data/prepare_species_gate_dataset.py.

Usage:
    python train_species_gate.py                                  # full run, defaults
    python train_species_gate.py --epochs 2 --limit-per-class 150  # fast smoke test
"""

import argparse
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

import torch
import torch.nn as nn
from PIL import Image
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision.models import MobileNet_V3_Small_Weights, mobilenet_v3_small


SCRIPT_DIR = Path(__file__).resolve().parent
SPECIES_GATE_DIR = SCRIPT_DIR.parent / "data" / "species_gate"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}
IMAGE_SIZE = 224
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

VAL_FRACTION = 0.2
RANDOM_SEED = 42

# Marks checkpoints from this script so they're never mistaken for the main
# 30-class disease model's weights.
MODEL_TYPE = "species_gate"
ARCHITECTURE = "mobilenet_v3_small"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def build_sample_list(species_gate_dir):
    """Scan data/species_gate/<in_scope|out_of_scope>/ into a flat list of
    (image_path, class_index) pairs, plus the class_index -> name mapping."""
    if not species_gate_dir.is_dir():
        print(f"ERROR: {species_gate_dir} does not exist.")
        print("  -> Run data/prepare_species_gate_dataset.py first to build data/species_gate/.")
        sys.exit(1)

    class_names = sorted(p.name for p in species_gate_dir.iterdir() if p.is_dir())
    if not class_names:
        print(f"ERROR: no class folders found under {species_gate_dir}.")
        sys.exit(1)

    samples = []
    for class_index, class_name in enumerate(class_names):
        class_dir = species_gate_dir / class_name
        for entry in sorted(class_dir.iterdir()):
            if entry.is_file() and entry.suffix.lower() in IMAGE_EXTENSIONS:
                samples.append((entry, class_index))

    return samples, class_names


def limit_samples_per_class(samples, limit):
    """Randomly cap each class to at most `limit` samples, for fast smoke
    testing."""
    if limit is None:
        return samples

    by_class = defaultdict(list)
    for sample in samples:
        by_class[sample[1]].append(sample)

    rng = random.Random(RANDOM_SEED)
    limited = []
    for class_samples in by_class.values():
        if len(class_samples) > limit:
            class_samples = rng.sample(class_samples, limit)
        limited.extend(class_samples)
    return limited


def stratified_split(samples):
    """Split samples into train/val, stratified by class so both in_scope
    and out_of_scope get a proportional, non-empty slice of validation data."""
    paths = [s[0] for s in samples]
    labels = [s[1] for s in samples]

    train_paths, val_paths, train_labels, val_labels = train_test_split(
        paths, labels, test_size=VAL_FRACTION, stratify=labels, random_state=RANDOM_SEED
    )

    train_samples = list(zip(train_paths, train_labels))
    val_samples = list(zip(val_paths, val_labels))
    return train_samples, val_samples


def verify_split_covers_every_class(train_samples, val_samples, class_names):
    """Sanity check: confirm no class was accidentally left with zero
    validation (or training) images by the split above."""
    train_counts = Counter(label for _, label in train_samples)
    val_counts = Counter(label for _, label in val_samples)

    missing_train = [name for i, name in enumerate(class_names) if train_counts.get(i, 0) == 0]
    missing_val = [name for i, name in enumerate(class_names) if val_counts.get(i, 0) == 0]

    if missing_train or missing_val:
        print("WARNING: stratified split left classes without data:")
        for name in missing_train:
            print(f"  - {name}: 0 training images")
        for name in missing_val:
            print(f"  - {name}: 0 validation images")
    else:
        print(f"OK: all {len(class_names)} classes have both training and validation images.")

    return train_counts, val_counts


# ---------------------------------------------------------------------------
# Augmentation
# ---------------------------------------------------------------------------
# A single standard augmentation pipeline is used for both classes -- unlike
# model/train.py's per-class augmentation boost for underrepresented disease
# classes, this dataset is roughly balanced (~1.18:1 in_scope:out_of_scope
# per the data-prep dry-run), so there's no small class that needs extra help.

def build_transforms():
    """Returns (train_transform, val_transform)."""
    train_transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])

    val_transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])

    return train_transform, val_transform


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------

class SpeciesGateDataset(Dataset):
    """Wraps a list of (path, label) pairs with a single shared transform."""

    def __init__(self, samples, transform):
        self.samples = samples
        self.transform = transform

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        image = Image.open(path).convert("RGB")
        return self.transform(image), label


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

def build_model(num_classes):
    model = mobilenet_v3_small(weights=MobileNet_V3_Small_Weights.IMAGENET1K_V1)
    in_features = model.classifier[-1].in_features
    model.classifier[-1] = nn.Linear(in_features, num_classes)
    return model


# ---------------------------------------------------------------------------
# Train / evaluate loops
# ---------------------------------------------------------------------------

def train_one_epoch(model, loader, optimizer, criterion, device):
    model.train()
    running_loss = 0.0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * images.size(0)

    return running_loss / len(loader.dataset)


def evaluate(model, loader, device, class_names):
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for images, labels in loader:
            images = images.to(device)
            outputs = model(images)
            preds = outputs.argmax(dim=1).cpu()
            all_preds.extend(preds.tolist())
            all_labels.extend(labels.tolist())

    report = classification_report(
        all_labels,
        all_preds,
        labels=list(range(len(class_names))),
        target_names=class_names,
        output_dict=True,
        zero_division=0,
    )
    return report


def print_per_class_report(report, class_names):
    print(f"\n{'Class':20s} {'Precision':>10s} {'Recall':>10s} {'F1':>10s} {'Support':>8s}")
    print("-" * 61)
    for name in class_names:
        metrics = report[name]
        print(
            f"{name:20s} {metrics['precision']:10.3f} {metrics['recall']:10.3f} "
            f"{metrics['f1-score']:10.3f} {int(metrics['support']):8d}"
        )
    print("-" * 61)
    print(f"Overall accuracy: {report['accuracy']:.3f}")
    print(f"Macro F1:         {report['macro avg']['f1-score']:.3f}")
    print(f"Weighted F1:      {report['weighted avg']['f1-score']:.3f}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Fine-tune MobileNetV3-Small on data/species_gate/ (binary in-scope/out-of-scope gate)."
    )
    parser.add_argument("--epochs", type=int, default=15)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument(
        "--limit-per-class",
        type=int,
        default=None,
        help="Cap each class to at most N images before splitting -- useful for a fast smoke test.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(SCRIPT_DIR / "species_gate_model.pt"),
        help="Where to save the trained model weights.",
    )
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    samples, class_names = build_sample_list(SPECIES_GATE_DIR)
    print(f"Found {len(samples)} images across {len(class_names)} classes in {SPECIES_GATE_DIR}")

    if args.limit_per_class is not None:
        samples = limit_samples_per_class(samples, args.limit_per_class)
        print(f"Limited to at most {args.limit_per_class} images/class -> {len(samples)} images total")

    train_samples, val_samples = stratified_split(samples)
    train_counts, val_counts = verify_split_covers_every_class(train_samples, val_samples, class_names)
    print(f"Train: {len(train_samples)} images, Val: {len(val_samples)} images")

    train_transform, val_transform = build_transforms()

    train_dataset = SpeciesGateDataset(train_samples, train_transform)
    val_dataset = SpeciesGateDataset(val_samples, val_transform)

    train_loader = DataLoader(
        train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=args.num_workers
    )
    val_loader = DataLoader(
        val_dataset, batch_size=args.batch_size, shuffle=False, num_workers=args.num_workers
    )

    model = build_model(len(class_names)).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    for epoch in range(1, args.epochs + 1):
        train_loss = train_one_epoch(model, train_loader, optimizer, criterion, device)
        print(f"\nEpoch {epoch}/{args.epochs} -- train loss: {train_loss:.4f}")

    print("\nFinal validation results:")
    report = evaluate(model, val_loader, device, class_names)
    print_per_class_report(report, class_names)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "class_names": class_names,
            "model_type": MODEL_TYPE,
            "architecture": ARCHITECTURE,
        },
        output_path,
    )
    print(f"\nSaved species-gate model weights to {output_path}")
    print(f"(model_type='{MODEL_TYPE}', architecture='{ARCHITECTURE}' -- distinct from the main disease model)")


if __name__ == "__main__":
    main()
