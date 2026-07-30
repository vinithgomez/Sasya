# Sasya — AI-powered plant disease detection for Indian crops

Upload a photo of a crop leaf, get back a diagnosis, a confidence score, and a sourced treatment recommendation — built for the crops and diseases that matter to Indian agriculture, not the generic US-centric datasets most similar projects use.

*Sasya is Sanskrit for "plant/crop" — short, distinctive, and fits the project's regional-India angle. The trained model itself is nicknamed **KrishiVision** ("krishi" meaning agriculture in Hindi and other Sanskrit-rooted Indian languages — a common naming convention in Indian agtech).*

Sasya is an application that classifies plant diseases across 7 regionally significant Indian crops — tomato, chili, potato, corn, rice, sugarcane, and cotton — spanning 30 disease/healthy classes. Rather than relying on a single off-the-shelf dataset, it merges three sources to genuinely cover these crops, including diseases (like Cotton Leaf Curl Virus) that are specific to the Indian subcontinent and absent from most global training sets. The trained model, KrishiVision (EfficientNet-B0, fine-tuned via transfer learning), reaches **98.5% overall accuracy** across all 30 classes. Treatment recommendations are sourced primarily from TNAU (Tamil Nadu Agricultural University) and other Indian agricultural institutions, with every non-Indian source explicitly flagged rather than silently blended in.

## Demo

<!-- TODO: add screenshot of the upload flow and results card here -->

<!-- TODO: add a demo GIF here, if one is recorded -->

## Key Features

- **Real-time disease classification** — upload a leaf photo, get a prediction in seconds
- **Confidence scoring** — every prediction includes the model's actual softmax confidence, not just a label
- **Sourced treatment recommendations** — causal organism, symptoms, and management steps for all 30 classes, cited back to TNAU/Indian agricultural sources (or explicitly flagged when a non-Indian source was used)
- **Honest "healthy" handling** — healthy classes return a clear no-action message instead of a fabricated treatment
- **Clean error handling** — non-image uploads and corrupted/unreadable files are rejected with a clear message, not a crash
- **Visible loading state** — spinner + status text while inference runs, so the UI never looks frozen

## Tech Stack

**Frontend**
- React + Vite
- TailwindCSS

**Backend**
- FastAPI
- PyTorch / TorchVision (model inference)

**ML**
- EfficientNet-B0 (ImageNet-pretrained, fine-tuned via transfer learning)
- Stratified train/val split, class-weighted loss, and extra augmentation for underrepresented classes

**Data**
- PlantVillage, Five Crop Diseases Dataset, and Cotton Leaf Disease Dataset, merged into 30 unified classes (~32.7k images)

## Model Performance

Trained for 15 epochs on GPU, all 30 classes, the full ~32.7k-image dataset (80/20 stratified split).

| Metric | Score |
|---|---|
| Overall accuracy | **98.5%** |
| Macro F1 | 98.2% |
| Weighted F1 | 98.5% |

Most classes score **0.98–1.000 F1** — including all 4 Cotton classes, all 3 Sugarcane classes, and 8 of 10 Tomato classes at perfect or near-perfect scores.

**Known limitation, documented honestly:** Rice is the one weak spot. `Rice_Brown_Spot` (F1 0.811) and `Rice_Leaf_Blast` (F1 0.856, missing ~20% of true blast cases) are confused with each other and with `Rice_Healthy`, while `Rice_Neck_Blast` is unaffected (F1 1.000) — so this isn't "Rice is hard" in general, it's specific to these two visually-similar early-stage fungal lesions. Confusion-matrix analysis (in `CLAUDE.md`) suggests this is more about under-detecting subtle early symptoms than pure disease-vs-disease confusion. This is called out here rather than hidden — full analysis and reasoning is in [CLAUDE.md](CLAUDE.md).

## Dataset Sources

Three datasets are merged to cover the target crop list:

- **PlantVillage** — tomato, chili (bell pepper proxy), potato, corn
- **Five Crop Diseases Dataset** — rice, sugarcane
- **Cotton Leaf Disease Dataset** — cotton

See [data/README.md](data/README.md) for full sourcing details, licenses, and the complete class-mapping table.

## Setup / Installation

### Backend

```bash
cd backend
python -m venv venv
./venv/Scripts/pip install -r requirements.txt
./venv/Scripts/python -m uvicorn app.main:app --port 8000
```

The backend loads the trained model (`model/krishivision_model.pt`) once at startup and serves predictions at `POST /predict`. Note: model weights are not included in this repo (gitignored, too large) — see [model/README.md](model/README.md) for training your own.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Starts the dev server at `http://localhost:5174` (pinned in `vite.config.js`). Expects the backend at `http://localhost:8000` by default — see `frontend/.env.example` to change it.

### Dataset prep (optional — only needed to retrain)

Raw datasets aren't included in the repo (too large, mixed licensing). See [data/README.md](data/README.md) for download sources, then:

```bash
python data/prepare_dataset.py --dry-run   # sanity-check the class mapping
python data/prepare_dataset.py             # merge into data/processed/
```

### Model training (optional — only needed to retrain)

See [model/README.md](model/README.md) for setup notes.

```bash
cd model
python train.py --epochs 2 --limit-per-class 150   # fast smoke test
python train.py                                     # full run
```

## Project Structure

```
.
├── backend/                     # FastAPI app — /predict endpoint, model inference, treatment lookup
│   └── app/
│       ├── main.py               # API + inference logic
│       └── treatment_data.json   # structured treatment recommendations for all 30 classes
├── frontend/                     # React + Vite upload UI
├── model/                        # training script (train.py) + docs
├── data/                         # dataset merge script + docs (raw/processed data itself is gitignored)
└── CLAUDE.md                     # full project spec, decisions, and detailed training results
```

## License

No license has been chosen yet — all rights reserved for now. An open-source license may be added later.

## Acknowledgments

Treatment recommendations and disease information sourced primarily from:

- **[TNAU Agritech Portal](https://agritech.tnau.ac.in/)** (Tamil Nadu Agricultural University) — the primary source for the large majority of classes
- **eAGRI** — Indian agricultural university e-course repository, used for select Cotton classes
- **AICRIP / IRRI** (All India Coordinated Rice Improvement Project / International Rice Research Institute) — cited via TNAU's Rice Blast documentation
- **[PlantVillage](https://plantvillage.psu.edu/)** dataset (Hughes & Salathé) — primary image source for Tomato, Chili, Potato, and Corn classes
- Additional international extension/research sources (Clemson HGIC, UMass Amherst, University of Kentucky, University of Florida IFAS, Pioneer Seeds) — used only where Indian-specific sources weren't found, and explicitly flagged as such wherever they appear

Full sourcing detail and transparency notes for every class are in [data/treatment_recommendations/](data/treatment_recommendations/) and [data/README.md](data/README.md).
