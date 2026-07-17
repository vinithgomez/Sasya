# CLAUDE.md — AI Plant Disease Detection

This file is persistent project memory for Claude Code. Read this first in every session. Update it as decisions are made — don't let it go stale.

## Project Overview

Final-year software project: an AI-powered plant disease/pest detection system for crops, with treatment recommendations. Pure software approach (no custom hardware/robotics). Built for portfolio impact as well as academic submission.

**Core flow**: User uploads or streams a photo of a crop leaf → model classifies disease/pest/healthy → app returns diagnosis + confidence + treatment recommendation.

**Differentiator (locked)**:
- [x] Regional Indian crop focus (rice, cotton, tomato, chili, sugarcane — confirm exact list at dataset stage) — fine-tuned/curated over generic US datasets

## Tech Stack

- **Model**: Transfer learning on EfficientNet or YOLOv8 (fine-tuned, not trained from scratch)
- **Datasets**: PlantVillage (primary, ~54k labeled images, 38 classes), PlantDoc (real-world/messier, for robustness), DeepWeeds/Weed25 (if weed detection is in scope)
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

## Open Questions / Not Yet Decided

- Exact crop/class list for the regional Indian focus (rice, cotton, tomato, chili, sugarcane are candidates) — decide at dataset stage.
- Classification-only vs. object detection (bounding boxes) — detection is more impressive for demo but harder to fine-tune and slower to iterate on.
- Whether weed detection is in scope or disease/pest only.
