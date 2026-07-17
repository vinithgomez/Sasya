# Dataset Setup

Raw image data is **not** committed to this repo (too large). This document describes how to get it locally for training.

## Primary dataset: PlantVillage

~54,000 labeled leaf images across 38 classes (14 crop species, healthy + diseased states).

**Download options:**

1. Kaggle (recommended, easiest):
   ```
   kaggle datasets download -d abdallahalidev/plantvillage-dataset
   ```
   Requires a Kaggle account and API token (`~/.kaggle/kaggle.json`). See https://www.kaggle.com/docs/api.

2. Direct from the original GitHub mirror:
   https://github.com/spMohanty/PlantVillage-Dataset

Unzip into `data/raw/plantvillage/` so it matches the structure below.

## Secondary dataset: PlantDoc

Real-world (non-lab, messier backgrounds) images — used later for robustness testing/fine-tuning, since PlantVillage alone is lab-condition and doesn't generalize well to phone photos.

- https://github.com/pratikkayal/PlantDoc-Dataset

Unzip into `data/raw/plantdoc/`.

## Regional Indian crop focus

Per the locked differentiator (see `../CLAUDE.md`), the final training set should be curated/filtered toward crops relevant to Indian agriculture (candidates: rice, cotton, tomato, chili, sugarcane — finalize list once class distributions are reviewed). This may mean:

- Filtering PlantVillage to the overlapping classes for these crops.
- Supplementing with additional regional datasets if PlantVillage coverage is thin (e.g. rice blast, cotton bollworm) — to be sourced and documented here once identified.

## Expected folder structure

```
data/
├── README.md
├── raw/                        # gitignored — downloaded, untouched source data
│   ├── plantvillage/
│   │   ├── Apple___Apple_scab/
│   │   ├── Apple___Black_rot/
│   │   ├── ...                 # one folder per class
│   └── plantdoc/
│       ├── train/
│       └── test/
└── processed/                  # gitignored — cleaned/split data ready for training
    ├── train/
    ├── val/
    └── test/
```

## Next steps (not done yet)

1. Download PlantVillage via Kaggle.
2. Inspect class list, identify which classes map to the target regional crops.
3. Write a prep script (`data/prepare.py`) to filter + split into `data/processed/`.
