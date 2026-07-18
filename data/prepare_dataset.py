#!/usr/bin/env python3
"""
Merge the three raw crop-disease datasets (PlantVillage, Five Crop Diseases,
Cotton Leaf Disease) into data/processed/<unified_class>/, following the
class mapping table documented in data/README.md.

Usage:
    python prepare_dataset.py             # actually copy files
    python prepare_dataset.py --dry-run   # only report what would be copied

Requires Pillow (pip install pillow) for corrupted-image detection.
"""

import argparse
import shutil
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("This script requires Pillow. Install it with: pip install pillow")
    sys.exit(1)


SCRIPT_DIR = Path(__file__).resolve().parent
RAW_DIR = SCRIPT_DIR / "raw"
PROCESSED_DIR = SCRIPT_DIR / "processed"

# Where each of the three raw dataset archives is expected to be unpacked.
SOURCE_ROOTS = {
    "plantvillage": RAW_DIR / "plantvillage",
    "five-crop-diseases": RAW_DIR / "five-crop-diseases",
    "cotton-disease": RAW_DIR / "cotton-disease",
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}

UNDERREPRESENTED_THRESHOLD = 200

# Unified class name -> (source key, documented source folder name).
# Source folder names are exactly as listed in the mapping table in
# data/README.md. A value of None means the README doesn't have a confirmed
# folder name yet -- the script reports this explicitly rather than guessing.
CLASS_MAPPING = {
    "Tomato_Bacterial_Spot": ("plantvillage", "Tomato___Bacterial_spot"),
    "Tomato_Early_Blight": ("plantvillage", "Tomato___Early_blight"),
    "Tomato_Late_Blight": ("plantvillage", "Tomato___Late_blight"),
    "Tomato_Leaf_Mold": ("plantvillage", "Tomato___Leaf_Mold"),
    "Tomato_Septoria_Leaf_Spot": ("plantvillage", "Tomato___Septoria_leaf_spot"),
    "Tomato_Spider_Mites": ("plantvillage", "Tomato___Spider_mites Two-spotted_spider_mite"),
    "Tomato_Target_Spot": ("plantvillage", "Tomato___Target_Spot"),
    "Tomato_Yellow_Leaf_Curl_Virus": ("plantvillage", "Tomato___Tomato_Yellow_Leaf_Curl_Virus"),
    "Tomato_Mosaic_Virus": ("plantvillage", "Tomato___Tomato_mosaic_virus"),
    "Tomato_Healthy": ("plantvillage", "Tomato___healthy"),
    "Chili_Bacterial_Spot": ("plantvillage", "Pepper,_bell___Bacterial_spot"),
    "Chili_Healthy": ("plantvillage", "Pepper,_bell___healthy"),
    "Potato_Early_Blight": ("plantvillage", "Potato___Early_blight"),
    "Potato_Late_Blight": ("plantvillage", "Potato___Late_blight"),
    "Potato_Healthy": ("plantvillage", "Potato___healthy"),
    "Corn_Common_Rust": ("plantvillage", "Corn_(maize)___Common_rust_"),
    "Corn_Gray_Leaf_Spot": ("plantvillage", "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot"),
    "Corn_Northern_Leaf_Blight": ("plantvillage", "Corn_(maize)___Northern_Leaf_Blight"),
    "Corn_Healthy": ("plantvillage", "Corn_(maize)___healthy"),
    "Rice_Brown_Spot": ("five-crop-diseases", "Rice___Brown_Spot"),
    "Rice_Leaf_Blast": ("five-crop-diseases", "Rice___Leaf_Blast"),
    "Rice_Neck_Blast": ("five-crop-diseases", "Rice___Neck_Blast"),
    "Rice_Healthy": ("five-crop-diseases", "Rice___Healthy"),
    "Sugarcane_Red_Rot": ("five-crop-diseases", "Sugarcane__Red_Rot"),
    "Sugarcane_Bacterial_Blight": ("five-crop-diseases", "Sugarcane__Bacterial Blight"),
    "Sugarcane_Healthy": ("five-crop-diseases", "Sugarcane__Healthy"),
    "Cotton_Bacterial_Blight": ("cotton-disease", "bacterial_blight"),
    "Cotton_Curl_Virus": ("cotton-disease", "curl_virus"),
    "Cotton_Fusarium_Wilt": ("cotton-disease", "fussarium_wilt"),  # source folder misspells "fusarium"
    "Cotton_Healthy": ("cotton-disease", "healthy"),
}


def normalize_folder_name(name):
    """Lowercase and strip punctuation/spacing so minor naming differences
    (case, extra underscores, commas, etc.) don't cause a false 'missing'."""
    return "".join(ch.lower() for ch in name if ch.isalnum())


def find_source_folder(source_root, documented_name):
    """Locate the actual subfolder under source_root that corresponds to
    documented_name, without assuming it matches exactly. Returns the
    resolved Path, or None if no match could be found."""
    if documented_name is None:
        return None

    exact_match = source_root / documented_name
    if exact_match.is_dir():
        return exact_match

    target = normalize_folder_name(documented_name)
    for entry in source_root.iterdir():
        if entry.is_dir() and normalize_folder_name(entry.name) == target:
            return entry

    return None


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


def check_source_roots_exist():
    """Fail fast with a clear message if a whole raw dataset folder is
    missing, rather than discovering it one class at a time partway through."""
    missing = [(key, path) for key, path in SOURCE_ROOTS.items() if not path.is_dir()]
    if not missing:
        return

    print("ERROR: missing expected raw dataset folder(s):\n")
    for key, path in missing:
        print(f"  - '{key}' not found at: {path}")
    print("\nDownload and unpack the corresponding dataset there (see data/README.md) before running this script.")
    sys.exit(1)


def process_class(unified_class, source_key, documented_name, dry_run):
    """Copy every valid image for one unified class from its source folder
    into data/processed/<unified_class>/. Returns the number of images
    copied (or that would be copied, in dry-run mode), or None on error."""
    source_root = SOURCE_ROOTS[source_key]
    source_folder = find_source_folder(source_root, documented_name)

    if source_folder is None:
        if documented_name is None:
            print(f"  ERROR: no confirmed source folder name for '{unified_class}' yet.")
            print(f"    -> Inspect {source_root} manually, then fill in the folder name")
            print(f"       for this class in CLASS_MAPPING in this script.")
        else:
            available = sorted(p.name for p in source_root.iterdir() if p.is_dir())
            print(f"  ERROR: could not find a folder matching '{documented_name}' under {source_root}.")
            print(f"    -> Folders actually present there: {available}")
        return None

    dest_dir = PROCESSED_DIR / unified_class
    copied = 0
    skipped = 0

    for entry in sorted(source_folder.iterdir()):
        if not entry.is_file():
            continue

        if not is_image_file(entry):
            skipped += 1
            continue

        if not is_valid_image(entry):
            print(f"    skipping corrupted image: {entry.name}")
            skipped += 1
            continue

        if dry_run:
            copied += 1
        else:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(entry, dest_dir / entry.name)
            copied += 1

    action = "would copy" if dry_run else "copied"
    print(f"  {action} {copied} image(s) from {source_folder.name}  ({skipped} skipped)")
    return copied


def print_summary(class_counts, dry_run):
    verb = "would contain" if dry_run else "contains"
    print("\n" + "=" * 70)
    print(f"SUMMARY -- data/processed/ {verb}:")
    print("=" * 70)

    for unified_class, count in class_counts.items():
        flag = ""
        if count < UNDERREPRESENTED_THRESHOLD:
            flag = "  <- underrepresented, may need augmentation"
        print(f"  {unified_class:35s} {count:6d} image(s){flag}")

    total = sum(class_counts.values())
    print("-" * 70)
    print(f"  {'TOTAL':35s} {total:6d} image(s)")


def main():
    parser = argparse.ArgumentParser(
        description="Merge raw crop-disease datasets into data/processed/, per the class mapping in data/README.md."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List what would be copied without actually copying anything.",
    )
    args = parser.parse_args()

    if args.dry_run:
        print("=== DRY RUN -- no files will be copied ===\n")

    check_source_roots_exist()

    class_counts = {}
    had_errors = False

    for unified_class, (source_key, documented_name) in CLASS_MAPPING.items():
        print(f"[{unified_class}]")
        count = process_class(unified_class, source_key, documented_name, args.dry_run)
        if count is None:
            had_errors = True
            class_counts[unified_class] = 0
        else:
            class_counts[unified_class] = count

    print_summary(class_counts, args.dry_run)

    if had_errors:
        print("\nOne or more classes had errors -- see ERROR lines above. Fix the source data or CLASS_MAPPING and re-run.")
        sys.exit(1)


if __name__ == "__main__":
    main()
