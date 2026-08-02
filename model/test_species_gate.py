#!/usr/bin/env python3
"""
Standalone verification tool for model/species_gate_model.pt -- the binary
in-scope/out-of-scope species gate. Loads the trained model and classifies
one or more arbitrary image files. Does not touch, import from, or otherwise
interact with backend/app/main.py or the /predict endpoint in any way.

Usage:
    python test_species_gate.py path/to/image1.jpg path/to/image2.jpg ...
    python test_species_gate.py --model path/to/other_checkpoint.pt image.jpg
"""

import argparse
import sys
from pathlib import Path

import torch
import torch.nn.functional as F
from PIL import Image, UnidentifiedImageError
from torchvision import transforms
from torchvision.models import mobilenet_v3_small

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_MODEL_PATH = SCRIPT_DIR / "species_gate_model.pt"

IMAGE_SIZE = 224
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

# Same preprocessing as train_species_gate.py's val_transform -- resize +
# normalize, no augmentation.
inference_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
])


def load_model(model_path):
    checkpoint = torch.load(model_path, map_location="cpu")
    class_names = checkpoint["class_names"]

    model = mobilenet_v3_small(weights=None)
    in_features = model.classifier[-1].in_features
    model.classifier[-1] = torch.nn.Linear(in_features, len(class_names))
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    model_type = checkpoint.get("model_type", "unknown")
    architecture = checkpoint.get("architecture", "unknown")
    return model, class_names, model_type, architecture


def classify_image(model, class_names, image_path):
    try:
        image = Image.open(image_path).convert("RGB")
    except (UnidentifiedImageError, OSError) as e:
        return None, None, f"could not read image ({e})"

    input_tensor = inference_transform(image).unsqueeze(0)

    with torch.no_grad():
        logits = model(input_tensor)
        probabilities = F.softmax(logits, dim=1)[0]
        confidence, predicted_idx = torch.max(probabilities, dim=0)

    return class_names[predicted_idx.item()], float(confidence.item()), None


def main():
    parser = argparse.ArgumentParser(
        description="Classify image(s) as in_scope or out_of_scope using the trained species-gate model."
    )
    parser.add_argument("images", nargs="+", help="Path(s) to image file(s) to classify.")
    parser.add_argument(
        "--model",
        type=str,
        default=str(DEFAULT_MODEL_PATH),
        help="Path to the species-gate checkpoint (default: model/species_gate_model.pt).",
    )
    args = parser.parse_args()

    model_path = Path(args.model)
    if not model_path.is_file():
        print(f"ERROR: model checkpoint not found at {model_path}")
        sys.exit(1)

    model, class_names, model_type, architecture = load_model(model_path)
    print(
        f"Loaded {model_path.name} "
        f"(model_type='{model_type}', architecture='{architecture}', classes={class_names})\n"
    )

    for image_arg in args.images:
        image_path = Path(image_arg)
        if not image_path.is_file():
            print(f"{image_path}: ERROR - file not found")
            continue

        predicted_class, confidence, error = classify_image(model, class_names, image_path)
        if error:
            print(f"{image_path.name}: ERROR - {error}")
            continue

        print(f"{image_path.name}: {predicted_class}  (confidence: {confidence * 100:.1f}%)")


if __name__ == "__main__":
    main()
