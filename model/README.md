# Model

`train.py` fine-tunes EfficientNet-B0 (ImageNet pretrained) on `data/processed/` for the 30-class regional crop disease classifier. See `../CLAUDE.md` > Model Architecture Decision for the architecture rationale.

## Setup

```
python -m venv venv
./venv/Scripts/pip install -r requirements.txt
```

**Note on torch version**: this machine's Windows Application Control policy blocks the DLLs shipped in the latest CPU PyTorch wheel (`torch==2.13.0+cpu` failed with `OSError: [WinError 4551]`). `torch==2.9.0+cpu` / `torchvision==0.24.0+cpu` load cleanly and are what's actually installed in `venv/`. If you recreate the venv from `requirements.txt` (which is unpinned) on this machine, pin those versions explicitly:

```
pip install torch==2.9.0 torchvision==0.24.0 --index-url https://download.pytorch.org/whl/cpu
```

On a machine without that restriction, the latest versions should work fine.

## Usage

```
python train.py --epochs 2 --limit-per-class 150   # fast smoke test
python train.py                                     # full run, defaults
```

`--limit-per-class` caps each class at N images before the train/val split — useful for quickly sanity-checking the pipeline without waiting on the full ~32.7k-image dataset.

## Status

Smoke-tested 2026-07-18 (2 epochs, 150 images/class cap, ~4.3k images): stratified split correctly gave every one of the 30 classes non-zero train/val data, augmentation boost applied to the 5 classes with <400 training images (Sugarcane x3, Potato_Healthy, Tomato_Mosaic_Virus... at this capped size, most classes fell under the threshold since 120 < 400 — see script comments), weighted loss, training loop, and per-class F1 reporting all ran end-to-end without errors. Smoke-test weights were deleted after verification (not meaningful — trained on a tiny capped/subsampled slice for a couple epochs).

Full training run not yet done — next step is running `python train.py` without `--limit-per-class` for a real training pass.
