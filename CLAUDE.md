# CLAUDE.md — AI Plant Disease Detection

This file is persistent project memory for Claude Code. Read this first in every session. Update it as decisions are made — don't let it go stale.

## Project Overview

Final-year software project: an AI-powered plant disease/pest detection system for crops, with treatment recommendations. Pure software approach (no custom hardware/robotics). Built for portfolio impact as well as academic submission.

**Core flow**: User uploads or streams a photo of a crop leaf → model classifies disease/pest/healthy → app returns diagnosis + confidence + treatment recommendation.

**Differentiator (locked)**:
- [x] Regional Indian crop focus (tomato, chili, potato, corn, rice, sugarcane, cotton — confirmed) — fine-tuned/curated over generic US datasets

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

## Open Questions / Not Yet Decided

- Whether weed detection is in scope or disease/pest only.
