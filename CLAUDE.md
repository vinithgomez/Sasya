# CLAUDE.md — AI Plant Disease Detection

This file is persistent project memory for Claude Code. Read this first in every session. Update it as decisions are made — don't let it go stale.

## Project Overview

Final-year software project: an AI-powered plant disease/pest detection system for crops, with treatment recommendations. Pure software approach (no custom hardware/robotics). Built for portfolio impact as well as academic submission.

**Core flow**: User uploads or streams a photo of a crop leaf → model classifies disease/pest/healthy → app returns diagnosis + confidence + treatment recommendation.

**Differentiator (locked)**:
- [x] Regional Indian crop focus (tomato, chili, potato, corn, rice, sugarcane, cotton — confirmed) — fine-tuned/curated over generic US datasets

## Where Things Stand / How to Resume

_(Project paused 2026-07-19 — a deliberate time/priorities break, not a stall on a problem. Nothing below needs to be reconsidered on return; the approach and every decision so far are still considered correct.)_

**Done and verified:**
- Scaffolding complete and working end-to-end: FastAPI backend (placeholder `/predict`) and React + Vite + Tailwind frontend (upload/preview/analyze flow), verified working together in-browser.
- Dataset fully sourced and merged: 3 sources (PlantVillage, Five Crop Diseases Dataset, Cotton Leaf Disease Dataset) mapped into 30 unified classes and copied into `data/processed/` — confirmed as of this update: 30 class folders, 32,726 images total. See `data/README.md` for the full class mapping and `data/prepare_dataset.py` for the merge script (dry-run mode included).
- Model architecture decided and documented: EfficientNet-B0 transfer learning, image classification (not object detection) — see Model Architecture Decision below.
- `model/train.py` written and smoke-tested: stratified train/val split (verified no class ends up with zero validation images), heavier augmentation for underrepresented classes, class-weighted loss, per-class precision/recall/F1 logging. Smoke test (2 epochs, capped data) ran end-to-end with no errors.

**Not done — training has not been completed:**
- Only a 1-epoch timing run on the full dataset (CPU) has been done, purely to estimate duration: ~29 min/epoch, so a real 12–25 epoch run would take roughly 7–12 hours unattended on CPU. That single epoch already reached 95.8% validation accuracy, but with Rice and Sugarcane classes visibly underperforming (Rice_Leaf_Blast, Rice_Brown_Spot, Sugarcane_Red_Rot notably weaker than the rest) — worth specific attention once real training runs.
- No trained model checkpoint is committed to the project (correct — weights are gitignored regardless). A local, untracked artifact from that timing test (`model/epoch1_checkpoint.pt`) is sitting on disk for reference only — it is not a real trained model, don't load it expecting a usable classifier.
- Colab/GPU exploration (a notebook porting `train.py` for GPU training with Drive persistence) was set aside and removed from the repo — full training hasn't been run on either CPU or GPU yet.

**Immediate next step on resume:**
1. Decide CPU (slow, ~7–12 hrs unattended, no iteration room) vs. Colab GPU (fast, ~15–30 min, room to iterate) for the real training run, then actually run it.
2. Evaluate real per-class results once trained — Rice and Sugarcane are the classes to watch closely.
3. Replace the backend's dummy `/predict` response with real model inference.
4. Build the treatment-recommendation lookup table covering all 30 classes.
5. Frontend polish, real-world (non-lab-condition) photo testing, then deployment (see Tech Stack below for target platforms).

## Model Architecture Decision

**Locked: EfficientNet-B0, fine-tuned via transfer learning, image classification (not object detection).**

Rationale: the task is single-label classification (one photo → one of 30 disease/healthy classes), matching the dataset's structure (folder-per-class, no bounding box annotations). EfficientNet-B0 is simpler to train, lighter to deploy under GPU constraints, and well-documented for this exact PlantVillage-style task. YOLOv8 was considered and deliberately not used for the current scope — see stretch goal below.

**Future stretch goal (beyond current scope, not part of the final-year submission): YOLOv8 object detection.**
If the project continues past graduation/submission, YOLOv8 would enable real object-detection use cases the current classifier can't do:
- Localizing *where* on a leaf a disease is (bounding boxes around specific lesions/spots), not just a whole-image label
- Detecting and counting multiple affected plants/leaves in a single wide-angle field photo
- Multi-instance detection (e.g. several different pests/diseases visible in one frame)

This would require a new annotated dataset (bounding boxes, not folder labels) — the current PlantVillage/Five-Crop/Cotton data is not directly usable for YOLO training without re-annotation. Treat this as a distinct v2 initiative, not an incremental add-on to the current classifier.

## Tech Stack

- **Model**: EfficientNet-B0, fine-tuned via transfer learning (see Model Architecture Decision above)
- **Datasets**: Merged from three sources — PlantVillage (tomato, chili/bell pepper, potato, corn), Five Crop Diseases Dataset (rice, sugarcane), Cotton Leaf Disease Dataset (cotton). See `data/README.md` for the full class mapping. PlantDoc (real-world/messier, for robustness) and DeepWeeds/Weed25 (if weed detection is in scope) remain optional additions.
- **Backend**: FastAPI serving model inference
- **Frontend**: React + Vite + TailwindCSS
- **Treatment recommendation layer**: rules-based lookup table initially; optional Claude API (claude-sonnet-4-6) for natural-language, localized advice generation from raw classification labels
- **Deployment target**: Render/Railway for backend (check free-tier compute is sufficient for model inference — may need quantization); Vercel for frontend

## Standing Instructions (Conventions)

- **PUSH convention**: Never auto-commit. Only run `git add`/`git commit`/`git push` when the user explicitly types `PUSH`. Commit messages should be descriptive, no AI co-author attribution.
- **Model tiering**: Use standard effort for routine implementation; flag for Opus-level review only if a cross-file bug isn't resolved after two attempts.
- **Verify before shipping**: Cross-check dataset class labels, treatment recommendations, and any agricultural claims against authoritative sources (extension services, PlantVillage documentation) before presenting as final. Document discrepancies rather than silently resolving them.
- **Offline/cost-conscious default**: Prefer local/free inference paths in dev. If Claude API is used for treatment text generation, make sure there's a non-LLM fallback (static lookup table) so the app doesn't hard-depend on a paid API call per request.

## Project Structure (proposed — confirm/adjust on first session)

```
plant-disease-detection/
├── model/              # training scripts, fine-tuning notebooks, saved weights
├── backend/            # FastAPI app, inference endpoint, treatment lookup
├── frontend/           # React + Vite app
├── data/               # dataset download/prep scripts (not raw data — too large for repo)
└── CLAUDE.md
```

## Decision Log

_(Append dated entries here as real decisions get made — dataset choices, model architecture picks, differentiator selection, deployment issues, etc. Keep it short and factual.)_

- [Date] — Project initialized.
- 2026-07-17 — Differentiator locked: Regional Indian crop focus. Chosen over offline-first (higher architectural risk, better as a later stretch goal) and multi-modal (adds scope before core pipeline works). This is primarily a data/training-time decision and doesn't change the backend/frontend architecture.
- 2026-07-17 — Scaffolded project structure (model/, backend/, frontend/, data/). Backend: FastAPI with placeholder `/predict` endpoint returning a dummy response. Frontend: React + Vite + Tailwind, single upload page (image picker, preview, Analyze button, results card). data/README.md documents PlantVillage download steps (not downloaded yet). No model training this session.
- 2026-07-18 — Crop list confirmed: tomato, chili (bell pepper proxy), potato, corn, rice, sugarcane, cotton. Dataset sourcing finalized as a three-way merge — PlantVillage (tomato/chili/potato/corn), Five Crop Diseases Dataset (rice/sugarcane), Cotton Leaf Disease Dataset (cotton) — with a unified class naming scheme documented in `data/README.md`. Exact cotton-dataset folder names still need verification after download.
- 2026-07-18 — Cotton class list upgraded from 2 generic placeholder classes (`Cotton_Diseased_Leaf`, `Cotton_Healthy_Leaf`) to 4 specific classes (`Cotton_Bacterial_Blight`, `Cotton_Curl_Virus`, `Cotton_Fusarium_Wilt`, `Cotton_Healthy`) after confirming the actual downloaded dataset's folder names. `data/prepare_dataset.py` and `data/README.md` updated accordingly; dry run confirms all 30 unified classes now resolve correctly against `data/raw/` (~32.7k images total). Sugarcane classes remain the notable underrepresented group (100 images each). Correction: earlier entries in this log miscounted this as 28 classes — the correct total is 30 (Tomato 10, Chili 2, Potato 3, Corn 4, Rice 4, Sugarcane 3, Cotton 4).
- 2026-07-18 — Model architecture locked: EfficientNet-B0 transfer learning, image classification (not object detection). YOLOv8 object detection deferred to a future v2 stretch goal (requires re-annotated bounding-box data, out of scope for the final-year submission).
- 2026-07-19 — Project paused (time/priorities, not a technical blocker). A 1-epoch CPU timing run confirmed the training pipeline works and gave a duration estimate (~29 min/epoch); the Colab/GPU exploration notebook was removed from the repo since it wasn't going to be used before the pause. See "Where Things Stand / How to Resume" above for full detail.

## Open Questions / Not Yet Decided

- Whether weed detection is in scope or disease/pest only.
