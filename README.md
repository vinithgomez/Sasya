# Sasya — AI Plant Disease Detection

An AI-powered plant disease/pest detection system for crops, with treatment recommendations. Final-year software project focused on regional Indian crops rather than the generic US-centric datasets most similar projects use.

**Core flow**: user uploads a photo of a crop leaf → model classifies disease/pest/healthy → app returns diagnosis, confidence, and a treatment recommendation.

## Status: paused

This project is on hold as of 2026-07-19 (a time/priorities break, not a technical blocker). Scaffolding, dataset prep, and the training pipeline are done and verified; the model hasn't been trained yet. See [CLAUDE.md](CLAUDE.md) → "Where Things Stand / How to Resume" for the full breakdown of what's done and what's next.

## Differentiator

Regional Indian crop focus — tomato, chili, potato, corn, rice, sugarcane, and cotton — curated from three merged datasets rather than relying on a single generic (largely US-crop) dataset. See [data/README.md](data/README.md) for sourcing and the full class mapping.

## Tech stack

- **Model**: EfficientNet-B0, fine-tuned via transfer learning (image classification, 30 classes)
- **Backend**: FastAPI
- **Frontend**: React + Vite + TailwindCSS
- **Datasets**: PlantVillage, Five Crop Diseases Dataset, Cotton Leaf Disease Dataset (merged into 30 unified classes, ~32.7k images)

Full rationale and decisions are logged in [CLAUDE.md](CLAUDE.md).

## Project structure

```
.
├── backend/    # FastAPI app, /predict endpoint (currently a placeholder response)
├── frontend/   # React + Vite upload UI
├── data/       # dataset merge script + docs (raw/processed data itself is gitignored)
├── model/      # training script (train.py) + docs
└── CLAUDE.md   # full project spec, decisions, and current status
```

## Running it locally

### Backend

```
cd backend
python -m venv venv
./venv/Scripts/pip install -r requirements.txt
./venv/Scripts/python -m uvicorn app.main:app --port 8000
```

### Frontend

```
cd frontend
npm install
npm run dev
```

This starts the dev server at `http://localhost:5174` (pinned in `vite.config.js` to avoid a port conflict on the original dev machine — change it if you don't need that). The frontend expects the backend at `http://localhost:8000` by default (see `frontend/.env.example`).

### Dataset prep

Raw datasets aren't included in the repo (too large, mixed licensing). See [data/README.md](data/README.md) for download sources and folder layout, then:

```
python data/prepare_dataset.py --dry-run   # sanity-check the class mapping
python data/prepare_dataset.py             # actually merge into data/processed/
```

### Model training

See [model/README.md](model/README.md) for setup notes (including a pinned PyTorch version workaround for a Windows Application Control restriction encountered during development).

```
cd model
python train.py --epochs 2 --limit-per-class 150   # fast smoke test
python train.py                                     # full run
```

## License

Not yet decided — this is currently an academic project without a chosen open-source license.
