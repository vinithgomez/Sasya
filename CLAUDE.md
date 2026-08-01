# CLAUDE.md — AI Plant Disease Detection

This file is persistent project memory for Claude Code. Read this first in every session. Update it as decisions are made — don't let it go stale.

## Project Overview

Final-year software project: an AI-powered plant disease/pest detection system for crops, with treatment recommendations. Pure software approach (no custom hardware/robotics). Built for portfolio impact as well as academic submission.

**Core flow**: User uploads or streams a photo of a crop leaf → model classifies disease/pest/healthy → app returns diagnosis + confidence + treatment recommendation.

**Differentiator (locked)**:
- [x] Regional Indian crop focus (tomato, chili, potato, corn, rice, sugarcane, cotton — confirmed) — fine-tuned/curated over generic US datasets

## Where Things Stand / How to Resume

_(Project resumed 2026-07-27. Training is now complete — see Final Training Results below. Nothing here needs to be reconsidered; the approach and every decision so far are still considered correct.)_

**Done and verified:**
- Scaffolding complete and working end-to-end: FastAPI backend (placeholder `/predict`) and React + Vite + Tailwind frontend (upload/preview/analyze flow), verified working together in-browser.
- Dataset fully sourced and merged: 3 sources (PlantVillage, Five Crop Diseases Dataset, Cotton Leaf Disease Dataset) mapped into 30 unified classes and copied into `data/processed/` — confirmed as of this update: 30 class folders, 32,726 images total. See `data/README.md` for the full class mapping and `data/prepare_dataset.py` for the merge script (dry-run mode included).
- Model architecture decided and documented: EfficientNet-B0 transfer learning, image classification (not object detection) — see Model Architecture Decision below.
- `model/train.py` written and smoke-tested: stratified train/val split (verified no class ends up with zero validation images), heavier augmentation for underrepresented classes, class-weighted loss, per-class precision/recall/F1 logging.
- **Model training complete** (2026-07-27): full 15-epoch run on GPU (Colab), all 30 classes, full ~32.7k dataset. Overall accuracy 0.985, macro F1 0.982. Trained weights (`krishivision_model.pt`) are on disk at `model/` (gitignored, not committed). Known limitation: Rice classes — see Final Training Results below for the full table and the confusion-matrix analysis of the Rice weak spot.

**Not done — next up:**
- Backend `/predict` still needs to be wired to real inference (currently in progress).
- Treatment-recommendation lookup table covering all 30 classes not yet built.
- Frontend polish and real-world (non-lab-condition) photo testing not yet done.
- Deployment not yet done (see Tech Stack below for target platforms).

**Immediate next step:**
1. Replace the backend's dummy `/predict` response with real model inference (load `krishivision_model.pt` once at startup, apply the same preprocessing as validation, return predicted class + confidence).
2. Build the treatment-recommendation lookup table for all 30 classes.
3. Frontend polish, real-world photo testing, then deployment.

## Model Architecture Decision

**Locked: EfficientNet-B0, fine-tuned via transfer learning, image classification (not object detection).**

Rationale: the task is single-label classification (one photo → one of 30 disease/healthy classes), matching the dataset's structure (folder-per-class, no bounding box annotations). EfficientNet-B0 is simpler to train, lighter to deploy under GPU constraints, and well-documented for this exact PlantVillage-style task. YOLOv8 was considered and deliberately not used for the current scope — see stretch goal below.

**Future stretch goal (beyond current scope, not part of the final-year submission): YOLOv8 object detection.**
If the project continues past graduation/submission, YOLOv8 would enable real object-detection use cases the current classifier can't do:
- Localizing *where* on a leaf a disease is (bounding boxes around specific lesions/spots), not just a whole-image label
- Detecting and counting multiple affected plants/leaves in a single wide-angle field photo
- Multi-instance detection (e.g. several different pests/diseases visible in one frame)

This would require a new annotated dataset (bounding boxes, not folder labels) — the current PlantVillage/Five-Crop/Cotton data is not directly usable for YOLO training without re-annotation. Treat this as a distinct v2 initiative, not an incremental add-on to the current classifier.

## Future Enhancements

**True plant-vs-not-plant detection (beyond the current confidence/entropy proxy).** `/predict` now rejects low-confidence/high-entropy predictions as "uncertain" (see Out-of-Distribution Safeguard below), which catches most non-plant images the closed-set classifier would otherwise confidently misclassify. But this is a proxy based on how *unsure* the model's softmax output is, not genuine content-based detection — a flat/low-entropy input (e.g. a solid-color image) can still slip through with artificially high confidence, since the network was never trained to recognize "not a plant" as a category at all. A real fix would need a separate detector, either:
- Gating through a general-purpose pretrained classifier (e.g. an ImageNet-based model) to check for plant/vegetation-related categories before running the specialized 30-class model, or
- Training a dedicated binary "plant leaf vs not" classifier on a newly-sourced negative dataset (non-leaf photos, screenshots, random objects, etc.)

Explicitly out of scope for the current version — treat as a distinct future initiative alongside the YOLOv8 stretch goal above, not an incremental fix to the current threshold logic.

## Known Limitation: Out-of-Scope Crop Species

Manual testing revealed a distinct failure mode from the plant/not-plant OOD case: when given a real leaf photo from a crop species NOT in the 7 supported crops (tomato, chili, potato, corn, rice, sugarcane, cotton) — e.g. a pear or apple leaf — the model does not reject it or express uncertainty. Instead it confidently (99.5%+ in one observed case) misclassifies it as one of its known 30 classes, because the model has genuinely learned visual features that happen to resemble a trained class, so confidence/entropy is low and the existing OOD safeguard does not catch this.

This is fundamentally different from the plant/not-plant problem: the model isn't uncertain here, it's confidently wrong, because it has no concept of "species outside my training set" — it can only ever choose among its 30 trained classes.

No confidence-threshold adjustment can fix this, since the issue isn't miscalibration — it's that the model was never trained to recognize this input as out-of-scope at all.

**Supporting evidence:** a follow-up test showed the model can also falsely trigger on non-plant images that happen to contain plant-like visual elements in the background/scenery (e.g. a tree in a stylized image), while genuinely plant-free images (tested with a dark, textureless image) are correctly rejected by the OOD safeguard. This confirms the model pattern-matches on any plant-like visual features present in the image, rather than on whether a leaf is the actual photographed subject.

**Real fix (out of scope for current version):** a dedicated species-identification gate — a separate classifier trained to first verify the input belongs to one of the 7 supported crop species before running disease classification. This is distinct from and additional to the plant-vs-not-plant detector already noted above.

**Current mitigation:** implemented 2026-07-31 — the frontend upload page now states the 7 supported crops directly ("Supports: Tomato, Chili, Potato, Corn, Rice, Sugarcane, Cotton"), so users have some warning before uploading an unsupported species. This is a UI-copy mitigation only; nothing changed at the model level, and results for unsupported crop species should still not be trusted.

## Out-of-Distribution Safeguard

Added 2026-07-31: `/predict` computes the full softmax distribution (not just top-1) and rejects the prediction as `{"status": "uncertain", ...}` if either:
- top-1 confidence is below `CONFIDENCE_THRESHOLD` (0.80, raised from an initial 0.60 — see below), or
- normalized entropy (entropy ÷ log(30), so it's on a 0–1 scale regardless of class count) is above `NORMALIZED_ENTROPY_THRESHOLD` (0.5)

Calibration test (2026-07-31) against 6 non-plant images (solid color, random noise, a text screenshot, and three synthetic stand-ins for "object photo" / "person photo" / "anime-style image" — real stock photos weren't available, so these were procedurally generated and are an imperfect proxy) and 5 real plant images (Chili_Bacterial_Spot, Rice_Brown_Spot, Rice_Leaf_Blast, Tomato_Healthy, Cotton_Curl_Virus):

- **5 of 6 non-plant images correctly rejected at the original 0.60 threshold.** The miss: a flat solid-color image was accepted at 75% confidence, 0.30 normalized entropy — predicted `Corn_Healthy`. This is the known failure mode described in Future Enhancements above (low-entropy false confidence on content-free input), not a bug in the threshold logic itself.
- **5 of 5 real plant images correctly accepted**, confidence 0.90–1.00, entropy 0.00–0.15 — comfortably clear of both thresholds, no false rejections observed.

`CONFIDENCE_THRESHOLD` raised from 0.60 to **0.80** (2026-07-31) based on this data — all 5 real plant confidences were ≥0.90, so this catches the solid-color miss (0.75 < 0.80) at zero observed cost to real results. Still pending: manual verification with real (non-synthetic) non-plant photos, including the original anime image that motivated this feature, plus the user's own real leaf photos — the synthetic test set above is an imperfect proxy and this threshold isn't considered final until that manual check passes.

## Final Training Results (2026-07-27)

Full training run: 15 epochs, GPU (Colab), EfficientNet-B0 transfer learning, all 30 classes, full ~32.7k-image dataset (stratified 80/20 split, class-weighted loss, heavier augmentation for underrepresented classes — see `model/train.py`).

**Overall accuracy: 0.985 — Macro F1: 0.982 — Weighted F1: 0.985**

| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| Chili_Bacterial_Spot | 1.000 | 1.000 | 1.000 | 199 |
| Chili_Healthy | 0.997 | 1.000 | 0.998 | 296 |
| Corn_Common_Rust | 1.000 | 1.000 | 1.000 | 238 |
| Corn_Gray_Leaf_Spot | 0.960 | 0.932 | 0.946 | 103 |
| Corn_Healthy | 1.000 | 1.000 | 1.000 | 232 |
| Corn_Northern_Leaf_Blight | 0.965 | 0.980 | 0.972 | 197 |
| Cotton_Bacterial_Blight | 1.000 | 1.000 | 1.000 | 90 |
| Cotton_Curl_Virus | 1.000 | 1.000 | 1.000 | 83 |
| Cotton_Fusarium_Wilt | 1.000 | 1.000 | 1.000 | 84 |
| Cotton_Healthy | 1.000 | 1.000 | 1.000 | 85 |
| Potato_Early_Blight | 1.000 | 1.000 | 1.000 | 200 |
| Potato_Healthy | 1.000 | 0.967 | 0.983 | 30 |
| Potato_Late_Blight | 1.000 | 0.995 | 0.997 | 200 |
| Rice_Brown_Spot | 0.818 | 0.805 | 0.811 | 123 |
| Rice_Healthy | 0.890 | 0.980 | 0.933 | 298 |
| Rice_Leaf_Blast | 0.928 | 0.795 | 0.856 | 195 |
| Rice_Neck_Blast | 1.000 | 1.000 | 1.000 | 200 |
| Sugarcane_Bacterial_Blight | 1.000 | 1.000 | 1.000 | 20 |
| Sugarcane_Healthy | 1.000 | 1.000 | 1.000 | 20 |
| Sugarcane_Red_Rot | 1.000 | 1.000 | 1.000 | 20 |
| Tomato_Bacterial_Spot | 0.988 | 1.000 | 0.994 | 426 |
| Tomato_Early_Blight | 0.990 | 0.985 | 0.987 | 200 |
| Tomato_Healthy | 1.000 | 1.000 | 1.000 | 318 |
| Tomato_Late_Blight | 0.992 | 0.997 | 0.995 | 382 |
| Tomato_Leaf_Mold | 0.990 | 1.000 | 0.995 | 190 |
| Tomato_Mosaic_Virus | 0.987 | 1.000 | 0.993 | 75 |
| Tomato_Septoria_Leaf_Spot | 1.000 | 1.000 | 1.000 | 354 |
| Tomato_Spider_Mites | 0.997 | 1.000 | 0.999 | 335 |
| Tomato_Target_Spot | 0.996 | 0.989 | 0.993 | 281 |
| Tomato_Yellow_Leaf_Curl_Virus | 1.000 | 0.993 | 0.997 | 1072 |

### Known limitation: Rice classes (not silently fixed — documented honestly)

Every class hits F1 ≥ 0.93 except three Rice classes: **Rice_Brown_Spot (F1 0.811)** and **Rice_Leaf_Blast (F1 0.856, recall 0.795 — missing ~20% of true blast cases)**, with Rice_Healthy also mildly affected (F1 0.933, pulled down by precision 0.890 despite recall 0.980). This is not a data volume issue — these classes have 613–1488 training images, comfortably sized. Rice_Neck_Blast, by contrast, is perfect (F1 1.000), so this isn't "Rice is hard" generically.

**Confusion matrix evidence** (reproduced locally against `krishivision_model.pt` on the same stratified val split, 98.69% overall accuracy — close enough to the reported 98.5% to trust as the same split):

| True \ Predicted | Brown_Spot | Healthy | Leaf_Blast | Neck_Blast |
|---|---|---|---|---|
| Rice_Brown_Spot (n=123) | 110 | 8 | 5 | 0 |
| Rice_Healthy (n=298) | 3 | 292 | 3 | 0 |
| Rice_Leaf_Blast (n=195) | 19 | 21 | 155 | 0 |
| Rice_Neck_Blast (n=200) | 0 | 0 | 0 | 200 |

This is **not a clean two-way Brown_Spot↔Leaf_Blast confusion** as initially hypothesized — it's a three-way cluster also involving Rice_Healthy. Rice_Leaf_Blast is confused with Rice_Healthy (21 cases, 10.8%) slightly *more* than with Rice_Brown_Spot (19 cases, 9.7%); Rice_Brown_Spot is likewise confused with Healthy (8, 6.5%) more than with Leaf_Blast (5, 4.1%). Rice_Neck_Blast has zero confusion with any other Rice class — cleanly separated.

**Working theory**: this looks more like under-detection of subtle/early-stage lesions (misread as Healthy) than pure disease-vs-disease visual similarity, though genuine Brown_Spot/Leaf_Blast lesion similarity is also a real, separate contributor (19+5=24 cases confused directly between the two). Both mechanisms are plausible and not mutually exclusive. Flagging as an open limitation rather than a fixed problem — if revisited, worth investigating with a Rice-specific augmentation boost, more Rice training data, or a review of mislabeled/ambiguous source images, rather than assuming the fix is obvious.

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
- 2026-07-27 — Model training complete: 15 epochs, GPU (Colab), full 30-class/~32.7k-image dataset. Overall accuracy 0.985, macro F1 0.982, weighted F1 0.985 — see Final Training Results above for the full per-class table. Known limitation documented (not silently fixed): Rice_Brown_Spot (F1 0.811) and Rice_Leaf_Blast (F1 0.856) are the weak spots, confirmed via confusion matrix to be a three-way confusion cluster with Rice_Healthy (not a clean two-way Brown_Spot/Leaf_Blast confusion as initially hypothesized) — Rice_Neck_Blast is unaffected (F1 1.000). Trained weights (`krishivision_model.pt`) placed at `model/` locally, gitignored.

## Open Questions / Not Yet Decided

- Whether weed detection is in scope or disease/pest only.
