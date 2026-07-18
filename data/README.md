# Data — Regional Indian Crop Disease Datasets

This project merges **three sources** to cover the target crop list: tomato, chili (bell pepper proxy), potato, corn, rice, sugarcane, and cotton.

## Sources

### 1. PlantVillage (primary — tomato, chili/bell pepper, potato, corn)
- Kaggle mirror: search "PlantVillage Dataset" on Kaggle, or GitHub: `spMohanty/PlantVillage-Dataset`
- ~54,000 lab-condition images, 38 classes total (we only use a subset — see class mapping below)
- License: open for research use (cite Mohanty et al. 2016 if published)

### 2. Five Crop Diseases Dataset (rice + sugarcane)
- Kaggle: `shubham2703/five-crop-diseases-dataset`
- Already includes rice, sugarcane, corn, potato, wheat — we only pull rice + sugarcane classes from it since corn/potato are better covered by PlantVillage
- License: CC BY 4.0

### 3. Cotton Leaf Disease Dataset
- Kaggle: `seroshkarim/cotton-leaf-disease-dataset` — **confirmed source**, 4 classes: `bacterial_blight`, `curl_virus`, `fussarium_wilt` (sic — the dataset's own folder name misspells "fusarium"), `healthy`
- Alternative if more granularity is wanted later: `sabuktagin/dataset-for-cotton-leaf-disease-detection` (7-class, field-condition images)

## Target unified class list

All source folders get renamed into this single scheme when copied into `data/processed/`. Format: `Crop_Condition` (underscore-separated, matches PlantVillage convention).

| Unified class | Source | Source folder name |
|---|---|---|
| `Tomato_Bacterial_Spot` | PlantVillage | `Tomato___Bacterial_spot` |
| `Tomato_Early_Blight` | PlantVillage | `Tomato___Early_blight` |
| `Tomato_Late_Blight` | PlantVillage | `Tomato___Late_blight` |
| `Tomato_Leaf_Mold` | PlantVillage | `Tomato___Leaf_Mold` |
| `Tomato_Septoria_Leaf_Spot` | PlantVillage | `Tomato___Septoria_leaf_spot` |
| `Tomato_Spider_Mites` | PlantVillage | `Tomato___Spider_mites Two-spotted_spider_mite` |
| `Tomato_Target_Spot` | PlantVillage | `Tomato___Target_Spot` |
| `Tomato_Yellow_Leaf_Curl_Virus` | PlantVillage | `Tomato___Tomato_Yellow_Leaf_Curl_Virus` |
| `Tomato_Mosaic_Virus` | PlantVillage | `Tomato___Tomato_mosaic_virus` |
| `Tomato_Healthy` | PlantVillage | `Tomato___healthy` |
| `Chili_Bacterial_Spot` | PlantVillage | `Pepper,_bell___Bacterial_spot` (bell pepper used as proxy — note this in the app UI/report) |
| `Chili_Healthy` | PlantVillage | `Pepper,_bell___healthy` |
| `Potato_Early_Blight` | PlantVillage | `Potato___Early_blight` |
| `Potato_Late_Blight` | PlantVillage | `Potato___Late_blight` |
| `Potato_Healthy` | PlantVillage | `Potato___healthy` |
| `Corn_Common_Rust` | PlantVillage | `Corn_(maize)___Common_rust_` |
| `Corn_Gray_Leaf_Spot` | PlantVillage | `Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot` |
| `Corn_Northern_Leaf_Blight` | PlantVillage | `Corn_(maize)___Northern_Leaf_Blight` |
| `Corn_Healthy` | PlantVillage | `Corn_(maize)___healthy` |
| `Rice_Brown_Spot` | Five Crop Diseases | `Rice___Brown_Spot` |
| `Rice_Leaf_Blast` | Five Crop Diseases | `Rice___Leaf_Blast` |
| `Rice_Neck_Blast` | Five Crop Diseases | `Rice___Neck_Blast` |
| `Rice_Healthy` | Five Crop Diseases | `Rice___Healthy` |
| `Sugarcane_Red_Rot` | Five Crop Diseases | `Sugarcane__Red_Rot` |
| `Sugarcane_Bacterial_Blight` | Five Crop Diseases | `Sugarcane__Bacterial Blight` |
| `Sugarcane_Healthy` | Five Crop Diseases | `Sugarcane__Healthy` |
| `Cotton_Bacterial_Blight` | Cotton dataset | `bacterial_blight` |
| `Cotton_Curl_Virus` | Cotton dataset | `curl_virus` |
| `Cotton_Fusarium_Wilt` | Cotton dataset | `fussarium_wilt` (source folder name is misspelled; unified class name is spelled correctly) |
| `Cotton_Healthy` | Cotton dataset | `healthy` |

**Note:** all source folder names above have been confirmed against the actual downloaded archives.

## Folder structure

```
data/
├── raw/                        # untouched downloads, gitignored
│   ├── plantvillage/
│   ├── five-crop-diseases/
│   └── cotton-disease/
├── processed/                  # unified class folders, gitignored
│   ├── Tomato_Bacterial_Spot/
│   ├── Tomato_Healthy/
│   ├── ...
│   └── Cotton_Healthy/
└── README.md                   # this file
```

Raw and processed data are **not committed to git** (too large, licensing mixed across sources) — only this README and any prep scripts live in version control. `data/raw/` and `data/processed/` should be in `.gitignore`.

## Prep steps

1. ~~Download all three sources into `data/raw/<source_name>/`.~~ Done.
2. ~~Write a script (`data/prepare_dataset.py`) that copies images from each source's original class folders into `data/processed/<unified_class_name>/`, per the mapping table above.~~ Done — run `python data/prepare_dataset.py --dry-run` to verify the mapping, then without `--dry-run` to actually copy.
3. Dry-run confirmed all 30 classes resolve correctly (~32.7k images total). Sugarcane classes are notably small (100 images each) — flagged as underrepresented, will need heavier augmentation. Cotton and all other classes are comfortably above the 200-image threshold.
4. Spot-check a handful of images per class after merging — confirm no mislabeled folders slipped through.
5. Only after this is done: move to model fine-tuning (EfficientNet or YOLOv8, per CLAUDE.md).
