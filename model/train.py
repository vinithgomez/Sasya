#!/usr/bin/env python3
"""
Fine-tune EfficientNet-B0 (ImageNet pretrained) on data/processed/ for the
30-class regional-crop disease classifier (see CLAUDE.md > Model Architecture
Decision). Uses a stratified train/val split, heavier augmentation for
underrepresented classes, and a class-weighted loss to address imbalance.

Usage:
    python train.py                                   # full run, defaults
    python train.py --epochs 2 --limit-per-class 150   # fast smoke test
"""

import argparse
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision.models import EfficientNet_B0_Weights, efficientnet_b0


SCRIPT_DIR = Path(__file__).resolve().parent
PROCESSED_DIR = SCRIPT_DIR.parent / "data" / "processed"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}
IMAGE_SIZE = 224
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

VAL_FRACTION = 0.2
RANDOM_SEED = 42

# Classes with fewer than this many images (before the train/val split) get
# the heavier augmentation pipeline. At current dataset sizes this covers
# Sugarcane's 3 classes (100 each), Potato_Healthy (152), and
# Tomato_Mosaic_Virus (373) -- the next smallest class, Cotton_Curl_Virus
# (417), is well clear of this line.
AUGMENTATION_BOOST_THRESHOLD = 400


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def build_sample_list(processed_dir):
    """Scan data/processed/<class>/ folders into a flat list of
    (image_path, class_index) pairs, plus the class_index -> name mapping."""
    if not processed_dir.is_dir():
        print(f"ERROR: {processed_dir} does not exist.")
        print("  -> Run data/prepare_dataset.py first to build data/processed/.")
        sys.exit(1)

    class_names = sorted(p.name for p in processed_dir.iterdir() if p.is_dir())
    if not class_names:
        print(f"ERROR: no class folders found under {processed_dir}.")
        sys.exit(1)

    samples = []
    for class_index, class_name in enumerate(class_names):
        class_dir = processed_dir / class_name
        for entry in sorted(class_dir.iterdir()):
            if entry.is_file() and entry.suffix.lower() in IMAGE_EXTENSIONS:
                samples.append((entry, class_index))

    return samples, class_names


def limit_samples_per_class(samples, limit):
    """Randomly cap each class to at most `limit` samples, for fast smoke
    testing. Classes already at or below the limit are left untouched, so
    naturally small classes (e.g. Sugarcane) keep their real, tiny counts."""
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
    """Split samples into train/val, stratified by class so every class
    (even a 100-image one like Sugarcane) gets a proportional, non-empty
    slice of validation data."""
    paths = [s[0] for s in samples]
    labels = [s[1] for s in samples]

    train_paths, val_paths, train_labels, val_labels = train_test_split(
        paths, labels, test_size=VAL_FRACTION, stratify=labels, random_state=RANDOM_SEED
    )

    train_samples = list(zip(train_paths, train_labels))
    val_samples = list(zip(val_paths, val_labels))
    return train_samples, val_samples


def verify_split_covers_every_class(train_samples, val_samples, class_names):
    """Sanity check requested explicitly: confirm no class was accidentally
    left with zero validation (or training) images by the split above."""
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

def build_transforms():
    """Returns (standard_train_transform, heavy_train_transform, val_transform)."""
    standard_train_transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])

    # Heavier augmentation for underrepresented classes: wider rotation,
    # added vertical flip and random affine jitter, stronger color jitter.
    heavy_train_transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.3),
        transforms.RandomRotation(35),
        transforms.ColorJitter(brightness=0.4, contrast=0.4),
        transforms.RandomAffine(degrees=0, translate=(0.1, 0.1), scale=(0.85, 1.15)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])

    val_transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])

    return standard_train_transform, heavy_train_transform, val_transform


def classes_needing_augmentation_boost(train_counts, class_names):
    boosted = {
        class_index
        for class_index, name in enumerate(class_names)
        if train_counts.get(class_index, 0) < AUGMENTATION_BOOST_THRESHOLD
    }
    print(f"\nClasses receiving heavier augmentation (< {AUGMENTATION_BOOST_THRESHOLD} training images):")
    for class_index in sorted(boosted):
        print(f"  - {class_names[class_index]} ({train_counts[class_index]} training images)")
    return boosted


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------

class PlantDiseaseDataset(Dataset):
    """Wraps a list of (path, label) pairs. Each label maps to its own
    transform via `transform_by_label`, so boosted classes can use the
    heavier augmentation pipeline while others use the standard one."""

    def __init__(self, samples, transform_by_label):
        self.samples = samples
        self.transform_by_label = transform_by_label

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        image = Image.open(path).convert("RGB")
        transform = self.transform_by_label[label]
        return transform(image), label


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

def build_model(num_classes):
    model = efficientnet_b0(weights=EfficientNet_B0_Weights.IMAGENET1K_V1)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    return model


def compute_class_weights(train_counts, num_classes):
    """Inverse-frequency class weights (sklearn's 'balanced' formula) to
    complement augmentation in addressing class imbalance in the loss."""
    labels_array = np.concatenate([
        np.full(train_counts.get(i, 0), i) for i in range(num_classes)
    ])
    weights = compute_class_weight(
        class_weight="balanced", classes=np.arange(num_classes), y=labels_array
    )
    return torch.tensor(weights, dtype=torch.float32)


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
    print(f"\n{'Class':35s} {'Precision':>10s} {'Recall':>10s} {'F1':>10s} {'Support':>8s}")
    print("-" * 76)
    for name in class_names:
        metrics = report[name]
        print(
            f"{name:35s} {metrics['precision']:10.3f} {metrics['recall']:10.3f} "
            f"{metrics['f1-score']:10.3f} {int(metrics['support']):8d}"
        )
    print("-" * 76)
    print(f"Overall accuracy: {report['accuracy']:.3f}")
    print(f"Macro F1:         {report['macro avg']['f1-score']:.3f}")
    print(f"Weighted F1:      {report['weighted avg']['f1-score']:.3f}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Fine-tune EfficientNet-B0 on data/processed/.")
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
        default=str(SCRIPT_DIR / "efficientnet_b0_plant_disease.pt"),
        help="Where to save the trained model weights.",
    )
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    samples, class_names = build_sample_list(PROCESSED_DIR)
    print(f"Found {len(samples)} images across {len(class_names)} classes in {PROCESSED_DIR}")

    if args.limit_per_class is not None:
        samples = limit_samples_per_class(samples, args.limit_per_class)
        print(f"Limited to at most {args.limit_per_class} images/class -> {len(samples)} images total")

    train_samples, val_samples = stratified_split(samples)
    train_counts, val_counts = verify_split_covers_every_class(train_samples, val_samples, class_names)
    print(f"Train: {len(train_samples)} images, Val: {len(val_samples)} images")

    boosted_labels = classes_needing_augmentation_boost(train_counts, class_names)
    standard_transform, heavy_transform, val_transform = build_transforms()

    train_transform_by_label = {
        i: (heavy_transform if i in boosted_labels else standard_transform)
        for i in range(len(class_names))
    }
    val_transform_by_label = {i: val_transform for i in range(len(class_names))}

    train_dataset = PlantDiseaseDataset(train_samples, train_transform_by_label)
    val_dataset = PlantDiseaseDataset(val_samples, val_transform_by_label)

    train_loader = DataLoader(
        train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=args.num_workers
    )
    val_loader = DataLoader(
        val_dataset, batch_size=args.batch_size, shuffle=False, num_workers=args.num_workers
    )

    model = build_model(len(class_names)).to(device)

    class_weights = compute_class_weights(train_counts, len(class_names)).to(device)
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    for epoch in range(1, args.epochs + 1):
        train_loss = train_one_epoch(model, train_loader, optimizer, criterion, device)
        print(f"\nEpoch {epoch}/{args.epochs} -- train loss: {train_loss:.4f}")

    print("\nFinal validation results:")
    report = evaluate(model, val_loader, device, class_names)
    print_per_class_report(report, class_names)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"model_state_dict": model.state_dict(), "class_names": class_names}, output_path)
    print(f"\nSaved model weights to {output_path}")


if __name__ == "__main__":
    main()
