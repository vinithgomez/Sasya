// Transcribed verbatim from CLAUDE.md > Final Training Results (2026-07-27).
// Do not edit these numbers without updating CLAUDE.md to match.

export const overallMetrics = {
  accuracy: 0.985,
  macroF1: 0.982,
  weightedF1: 0.985,
}

export const perClassResults = [
  { class: 'Chili_Bacterial_Spot', precision: 1.0, recall: 1.0, f1: 1.0, support: 199 },
  { class: 'Chili_Healthy', precision: 0.997, recall: 1.0, f1: 0.998, support: 296 },
  { class: 'Corn_Common_Rust', precision: 1.0, recall: 1.0, f1: 1.0, support: 238 },
  { class: 'Corn_Gray_Leaf_Spot', precision: 0.96, recall: 0.932, f1: 0.946, support: 103 },
  { class: 'Corn_Healthy', precision: 1.0, recall: 1.0, f1: 1.0, support: 232 },
  { class: 'Corn_Northern_Leaf_Blight', precision: 0.965, recall: 0.98, f1: 0.972, support: 197 },
  { class: 'Cotton_Bacterial_Blight', precision: 1.0, recall: 1.0, f1: 1.0, support: 90 },
  { class: 'Cotton_Curl_Virus', precision: 1.0, recall: 1.0, f1: 1.0, support: 83 },
  { class: 'Cotton_Fusarium_Wilt', precision: 1.0, recall: 1.0, f1: 1.0, support: 84 },
  { class: 'Cotton_Healthy', precision: 1.0, recall: 1.0, f1: 1.0, support: 85 },
  { class: 'Potato_Early_Blight', precision: 1.0, recall: 1.0, f1: 1.0, support: 200 },
  { class: 'Potato_Healthy', precision: 1.0, recall: 0.967, f1: 0.983, support: 30 },
  { class: 'Potato_Late_Blight', precision: 1.0, recall: 0.995, f1: 0.997, support: 200 },
  { class: 'Rice_Brown_Spot', precision: 0.818, recall: 0.805, f1: 0.811, support: 123 },
  { class: 'Rice_Healthy', precision: 0.89, recall: 0.98, f1: 0.933, support: 298 },
  { class: 'Rice_Leaf_Blast', precision: 0.928, recall: 0.795, f1: 0.856, support: 195 },
  { class: 'Rice_Neck_Blast', precision: 1.0, recall: 1.0, f1: 1.0, support: 200 },
  { class: 'Sugarcane_Bacterial_Blight', precision: 1.0, recall: 1.0, f1: 1.0, support: 20 },
  { class: 'Sugarcane_Healthy', precision: 1.0, recall: 1.0, f1: 1.0, support: 20 },
  { class: 'Sugarcane_Red_Rot', precision: 1.0, recall: 1.0, f1: 1.0, support: 20 },
  { class: 'Tomato_Bacterial_Spot', precision: 0.988, recall: 1.0, f1: 0.994, support: 426 },
  { class: 'Tomato_Early_Blight', precision: 0.99, recall: 0.985, f1: 0.987, support: 200 },
  { class: 'Tomato_Healthy', precision: 1.0, recall: 1.0, f1: 1.0, support: 318 },
  { class: 'Tomato_Late_Blight', precision: 0.992, recall: 0.997, f1: 0.995, support: 382 },
  { class: 'Tomato_Leaf_Mold', precision: 0.99, recall: 1.0, f1: 0.995, support: 190 },
  { class: 'Tomato_Mosaic_Virus', precision: 0.987, recall: 1.0, f1: 0.993, support: 75 },
  { class: 'Tomato_Septoria_Leaf_Spot', precision: 1.0, recall: 1.0, f1: 1.0, support: 354 },
  { class: 'Tomato_Spider_Mites', precision: 0.997, recall: 1.0, f1: 0.999, support: 335 },
  { class: 'Tomato_Target_Spot', precision: 0.996, recall: 0.989, f1: 0.993, support: 281 },
  { class: 'Tomato_Yellow_Leaf_Curl_Virus', precision: 1.0, recall: 0.993, f1: 0.997, support: 1072 },
]
