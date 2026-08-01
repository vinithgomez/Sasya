#!/usr/bin/env python3
"""
Builds the binary in-scope-vs-out-of-scope-species dataset for the planned
species-detection gate model, into data/species_gate/. Purely additive --
does not read-modify or write anything under data/raw/ or data/processed/.

Positive class ("in_scope"): every image already merged into data/processed/
(the 30 disease/healthy classes across our 7 supported crops: tomato, chili,
potato, corn, rice, sugarcane, cotton). Species and disease labels are
discarded here -- for this gate, all that matters is "this photo belongs to
one of our supported crop species."

Negative class ("out_of_scope"): PlantVillage species deliberately excluded
from the main classifier (Apple, Blueberry, Cherry, Grape, Orange, Peach,
Raspberry, Soybean, Squash, Strawberry) -- real leaf photos of different
species, already sitting in data/raw/plantvillage/ from the original
PlantVillage download; never copied into data/processed/ since they're
outside our 7-crop scope.

Usage:
    python prepare_species_gate_dataset.py --dry-run   # sanity-check counts
    python prepare_species_gate_dataset.py             # actually copy
"""

import argparse
import shutil
import sys
from pathlib import Path

from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
PROCESSED_DIR = SCRIPT_DIR / "processed"
RAW_PLANTVILLAGE_DIR = SCRIPT_DIR / "raw" / "plantvillage"
OUTPUT_DIR = SCRIPT_DIR / "species_gate"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}

IMBALANCE_WARNING_RATIO = 1.5

# PlantVillage species folders NOT among our 7 supported crops -- real leaf
# photos of different species, used as negative ("out of scope") examples.
# Confirmed present under data/raw/plantvillage/ as of this script's writing.
OUT_OF_SCOPE_FOLDERS = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
]


def is_image_file(path):
    return path.suffix.lower() in IMAGE_EXTENSIONS


def is_valid_image(path):
    """Returns False for anything Pillow can't open/decode, so corrupted
    files are skipped instead of crashing the run."""
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except Exception:
        return False


def collect_source_images(source_dirs):
    """Returns a list of (source_path, prefix) pairs across all given
    directories. The prefix (source folder name) travels with each image so
    copied filenames stay unique once everything is flattened into one
    destination folder (data/processed/ has 30 source folders, several of
    which could plausibly contain same-named files)."""
    samples = []
    for source_dir in source_dirs:
        if not source_dir.is_dir():
            print(f"ERROR: expected source folder not found: {source_dir}")
            sys.exit(1)
        for entry in sorted(source_dir.iterdir()):
            if entry.is_file() and is_image_file(entry):
                samples.append((entry, source_dir.name))
    return samples


def copy_class(label, samples, dry_run):
    dest_dir = OUTPUT_DIR / label
    copied = 0
    skipped = 0

    for source_path, prefix in samples:
        if not is_valid_image(source_path):
            print(f"    skipping corrupted image: {source_path}")
            skipped += 1
            continue

        dest_name = f"{prefix}__{source_path.name}"
        if dry_run:
            copied += 1
        else:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, dest_dir / dest_name)
            copied += 1

    return copied, skipped


def main():
    parser = argparse.ArgumentParser(
        description="Build the binary in-scope/out-of-scope species dataset into data/species_gate/."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Report counts without copying anything."
    )
    args = parser.parse_args()

    if args.dry_run:
        print("=== DRY RUN -- no files will be copied ===\n")

    action = "would copy" if args.dry_run else "copied"

    # --- Positive class: every image already merged into data/processed/ ---
    if not PROCESSED_DIR.is_dir():
        print(f"ERROR: {PROCESSED_DIR} does not exist -- run data/prepare_dataset.py first.")
        sys.exit(1)

    in_scope_class_dirs = sorted(p for p in PROCESSED_DIR.iterdir() if p.is_dir())
    in_scope_samples = collect_source_images(in_scope_class_dirs)

    print("[in_scope]")
    in_scope_copied, in_scope_skipped = copy_class("in_scope", in_scope_samples, args.dry_run)
    print(
        f"  {action} {in_scope_copied} image(s) from {len(in_scope_class_dirs)} classes "
        f"in data/processed/ ({in_scope_skipped} skipped)"
    )

    # --- Negative class: PlantVillage species outside our 7-crop scope ---
    out_of_scope_dirs = [RAW_PLANTVILLAGE_DIR / name for name in OUT_OF_SCOPE_FOLDERS]
    missing = [d for d in out_of_scope_dirs if not d.is_dir()]
    if missing:
        print("ERROR: expected out-of-scope source folder(s) not found:")
        for d in missing:
            print(f"  - {d}")
        sys.exit(1)

    out_of_scope_samples = collect_source_images(out_of_scope_dirs)

    print("\n[out_of_scope]")
    out_copied, out_skipped = copy_class("out_of_scope", out_of_scope_samples, args.dry_run)
    print(
        f"  {action} {out_copied} image(s) from {len(out_of_scope_dirs)} species folders "
        f"in data/raw/plantvillage/ ({out_skipped} skipped)"
    )

    # --- Class balance report ---
    total = in_scope_copied + out_copied
    print("\n=== Class balance ===")
    if total == 0:
        print("  Nothing copied -- both classes are empty. Check the source folders above.")
        sys.exit(1)

    in_scope_pct = in_scope_copied / total * 100
    out_scope_pct = out_copied / total * 100
    larger, smaller = max(in_scope_copied, out_copied), min(in_scope_copied, out_copied)
    ratio = larger / smaller if smaller > 0 else float("inf")

    print(f"  in_scope:     {in_scope_copied:6d} ({in_scope_pct:.1f}%)")
    print(f"  out_of_scope: {out_copied:6d} ({out_scope_pct:.1f}%)")
    print(f"  ratio: {ratio:.2f}:1")

    if ratio > IMBALANCE_WARNING_RATIO:
        larger_label = "in_scope" if in_scope_copied > out_copied else "out_of_scope"
        print(f"\n  WARNING: classes are imbalanced (>{IMBALANCE_WARNING_RATIO}:1, larger class is '{larger_label}').")
        print("  Consider subsampling the larger class or adding augmentation for the smaller one before training.")
    else:
        print(f"\n  OK: classes are within {IMBALANCE_WARNING_RATIO}:1 -- safe to proceed without rebalancing.")


if __name__ == "__main__":
    main()
