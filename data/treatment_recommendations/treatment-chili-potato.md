# Treatment Recommendations — Chili & Potato (Batch 2 of 6 crop groups)

## CHILI (2 classes)

Note: your dataset's "Chili" classes come from PlantVillage's "Pepper, bell" folders (bell pepper is a proxy for chili in the dataset, as discussed earlier). Good news: TNAU has a dedicated **Chilli** (not just bell pepper) disease page, so the sourced advice below is genuinely chili-specific and India-relevant, not just a bell-pepper stand-in.

### Chili_Bacterial_Spot
**Causal organism:** *Xanthomonas campestris pv. vesicatoria*
**Symptoms:** Small circular/irregular, dark brown to black greasy spots on leaves; spots enlarge with a lighter center surrounded by a dark band; spots coalesce into irregular lesions; severely affected leaves turn chlorotic and fall off; petioles and stems affected, stem infection causes cankerous growth and branch wilting; on fruit — round, raised, water-soaked spots with a pale yellow border that turn brown with a depressed center, sometimes showing bacterial ooze droplets.
**Management:**
- Spray mancozeb @ 2 g/litre or copper oxychloride @ 2.5 g/litre
- Seed treatment with 0.1% mercuric chloride solution for 2-5 minutes
- Seedlings may be sprayed with 1% Bordeaux mixture or 0.25% copper oxychloride
- Do not spray streptomycin after fruit formation begins
- Field sanitation important; obtain seeds only from disease-free plants
**Source:** TNAU Agritech Portal — https://agritech.tnau.ac.in/crop_protection/chilli_diseases_4.html

### Chili_Healthy
No treatment needed — app should return a positive/no-action message when this class is predicted.

---

## POTATO (3 classes)

### Potato_Early_Blight
**Causal organism:** *Alternaria solani*
**Symptoms:** Oval-to-angular dark brown/black "target" spots on leaflets with concentric rings of dead tissue, narrow chlorotic (yellowing) halo around each spot; lowest/oldest leaves infected first; can cause leaf droop and yield loss if severe; tuber lesions are less common than leaf infection but appear as sunken, dark, circular spots.
**Management:**
- Cultural: crop rotation, remove and destroy infected debris, avoid overhead irrigation, keep plants adequately fertilized (stressed plants are more susceptible)
- Chemical: Mancozeb is confirmed highly effective by field trials at an Indian agricultural university (S.D. Agricultural University, Gujarat) — applied as foliar spray @ 0.25% (with 1% urea) at 40-45 days crop age, repeated at 8-10 day intervals; for higher disease pressure, alternating with a systemic fungicide like hexaconazole 5 EC @ 0.05% between mancozeb sprays improved control further in the same trial
- Use resistant/late-maturing varieties where available
**Source:** Field trial conducted at Potato Research Station, S.D. Agricultural University, Deesa, India (2015-16 and 2016-17) — https://www.academia.edu/129963294 and https://www.academia.edu/116758209. **Note:** TNAU's own dedicated early blight page exists (agritech.tnau.ac.in) but blocked automated fetching — the Indian field-study source used here is a reasonable substitute since it's still India-specific, peer-relevant agricultural research rather than a generic global source.

### Potato_Late_Blight
**Causal organism:** *Phytophthora infestans*
**Symptoms:** Affects leaves, stems, and tubers. Water-soaked spots on leaves that enlarge, turning purple-brown then black; white fungal growth on the underside of leaves; spreads to petioles and stems, frequently developing at nodes, causing the stem to break and the plant to topple; tubers show purplish-brown spots that on cutting reveal rusty-brown necrosis spreading from the surface toward the center.
**Management:**
- Protective spraying with mancozeb or zineb @ 0.2% to prevent tuber infection
- Minimize tuber contamination by avoiding injury at harvest and not storing visibly infected tubers
- Recommended resistant varieties (India-specific): Kufri Naveen, Kufri Jeevan, Kufri Alenkar, Kufri Khasi Garo, Kufri Moti
- Destroy foliage a few days before harvest (via suitable herbicide) to reduce tuber contamination risk
- Favourable conditions to watch for: relative humidity >90%, temperature 10-25°C, night temperature ~10°C, cloudiness before rainfall
**Source:** TNAU Agritech Portal — https://agritech.tnau.ac.in/crop_protection/crop_prot_crop%20diseases_veg_potato_1.html

### Potato_Healthy
No treatment needed — app should return a positive/no-action message when this class is predicted.

---

## Sourcing summary for this batch

- **Chili (both classes):** fully TNAU-sourced, genuinely chili-specific (not a bell-pepper substitute at the source level, even though the training images are from a bell pepper dataset).
- **Potato Late Blight:** fully TNAU-sourced, including India-specific resistant variety names (Kufri series) — strong, authoritative match for this project's differentiator.
- **Potato Early Blight:** TNAU's own page exists but blocked automated access; substituted with a peer-reviewed Indian field trial (Gujarat) confirming the same core fungicide recommendation. This is a reasonable substitute, not a generic/US fallback, but worth noting the difference in source type (a single field study vs. TNAU's institutional page) if being fully precise in the project report.
