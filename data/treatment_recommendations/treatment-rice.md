# Treatment Recommendations — Rice (Batch 4 of 6 crop groups)

**Note of interest for this project:** Rice is your model's one documented weak spot (Brown Spot F1 0.811, Leaf Blast F1 0.856, per CLAUDE.md's Final Training Results). Worth reading these two entries with that in mind — the symptom descriptions below explain *why* a model might confuse them (both are fungal lesions with similar coloration/shape at early stages), which is useful context for your report.

## Rice_Brown_Spot
**Causal organism:** *Helminthosporium oryzae* (syn. *Drechslera oryzae*; sexual stage: *Cochliobolus miyabeanus*) — also called sesame leaf spot / Helminthosporiose / fungal blight
**Symptoms:** Starts as minute brown dots, becoming cylindrical-to-oval-to-circular, resembling sesame seeds (0.5-2.0mm), coalescing into large patches that dry up the leaf; also infects panicle/neck (brown coloration) and seeds (black/brown spots on glumes, covered by an olive velvety growth); infected seed causes germination failure, seedling mortality, and reduced grain quality/weight; up to 50% yield loss in severe cases. Attacks from seedling (nursery) stage through to milk stage in the main field.
**Favourable conditions:** 25-30°C, relative humidity above 80%, leaves wet 8-24 hours for infection; excess nitrogen aggravates it; notably common in nutrient-deficient or unflooded soils, rare in fertile, well-irrigated soils.
**Management:**
- *Cultural:* use disease-free seed (disease is seed-borne); remove alternate/collateral weed hosts; grow resistant varieties — **ADT 44, PY 4, CORH 1, CO 44, Cauvery, Bhavani, TPS 4, Dhanu**; ensure proper nutrition and avoid water stress (most important preventive factor); amend silicon-deficient soils with calcium silicate slag and irrigate well
- *Seed treatment:* *Pseudomonas fluorescens* @ 10g/kg seed + seedling dip @ 2.5kg/ha in 100L water for 30 min; OR Captan/Thiram @ 2.0g/kg seed; OR hot water seed treatment (53-54°C for 10-12 min, after pre-soaking in cold water 8 hours)
- *Chemical:* spray Mancozeb @ 2.0g/litre OR Edifenphos @ 1ml/litre, 2-3 times at 10-15 day intervals, preferably early morning or afternoon during flowering and post-flowering; tricyclazole seed treatment followed by mancozeb+tricyclazole spray at tillering and late booting stages also gives good control
**Source:** TNAU Agritech Portal (expert system) — http://www.agritech.tnau.ac.in/expert_system/paddy/cpdisbrownspot.html

## Rice_Leaf_Blast
## Rice_Neck_Blast
(TNAU treats Leaf Blast and Neck Blast as manifestations of one disease — "Blast" — at different plant sites, so both classes share the same causal organism/source and are documented together below, with site-specific symptoms called out separately.)

**Causal organism:** *Magnaporthe oryzae* (syn: *Pyricularia grisea*, *Magnaporthe grisea*)
**Symptoms — general:** attacks the crop from seedling to late tillering and ear-heading stages; appears on leaves, nodes, rachis, and glumes.
- **Leaf blast:** small bluish-green flecks that enlarge under moist conditions into spindle-shaped spots with a grey center and dark brown margin; spots coalesce, large leaf areas dry and wither; severely infected fields appear "burnt" from a distance.
- **Nodal blast:** black lesions girdle the nodes; affected nodes may break, killing all plant parts above the infected node.
- **Neck blast:** grayish-brown lesions on the neck, girdling it and causing the panicle to fall over; if infection occurs before the milky stage, no grain forms at all; later infection produces poor-quality grain.
**Favourable conditions:** intermittent drizzles, cloudy weather, high relative humidity (93-99%), low night temperature (15-20°C, or below 26°C), presence of collateral/alternate host weeds, excess nitrogen application.
**Collateral (alternate) hosts:** *Panicum repens, Digitaria magrginata, Brachiaria mutica, Leersia hexandra, Echinochloa crusgalli* — these grassy weeds harbor the fungus between rice crops.
**Management:**
- Grow resistant/moderately resistant varieties: **CO 47, CO 51, CO 52, CO 53, CO 55, CO 56, ASD 18, IR64**
- Remove and destroy weed hosts on field bunds and channels
- Seed treatment: Captan, Thiram, Carbendazim, or Tricyclazole @ 2g/kg seed, OR *Bacillus subtilis* @ 10g/kg seed
- Nursery spray: Carbendazim 50 WP @ 25g, or Edifenphos 50 EC @ 25ml, per 20-cent nursery
- Main field foliar spray (at first symptoms): Edifenphos @ 200ml/acre, OR Carbendazim @ 100g/acre, OR Tricyclazole 75 WP @ 200g/acre, OR Iprobenphos (IBP) @ 200ml/acre, OR azoxystrobin + difenoconazole @ 100ml/acre
**Source:** TNAU Agritech Portal, in partnership with AICRIP (All India Coordinated Rice Improvement Project) and IRRI (International Rice Research Institute, Philippines) — https://agritech.tnau.ac.in/crop_protection/rice_diseases/rice_1.html and https://agritech.tnau.ac.in/crop_protection/rice_diseases/another%20methods_rice_1.html

## Rice_Healthy
No treatment needed — app should return a positive/no-action message when this class is predicted.

---

## Sourcing summary for this batch

All 4 classes (3 disease + healthy) are **fully TNAU-sourced**, and Blast specifically cites TNAU's collaboration with AICRIP and IRRI — this is the single most authoritative batch so far, genuinely matching the project's India-specific differentiator. No gaps to flag here.

**One nuance worth carrying into your app copy or report:** TNAU documents Leaf Blast and Neck Blast as the *same underlying disease* (Magnaporthe oryzae) manifesting at different plant locations, sharing the same resistant varieties and chemical treatments. This is a genuinely useful fact — it means a misclassification between these two specific classes by your model is arguably less consequential in practice than it might first appear, since the recommended treatment is largely identical either way. Worth mentioning explicitly in your final report as a nuance on the "Rice weak spot" limitation — the model's confusion between visually similar early-stage lesions matters less for real-world usefulness when the underlying treatment guidance converges anyway.

---

## Running total across all batches so far

23 of 30 classes complete: Tomato (10), Chili (2), Potato (3), Corn (4), Rice (4).
Remaining: Sugarcane (3), Cotton (4) — 7 classes left across 2 crop groups.
