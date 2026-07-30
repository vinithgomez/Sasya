# Treatment Recommendations — Corn/Maize (Batch 3 of 6 crop groups)

## Corn_Common_Rust
**Causal organism:** *Puccinia sorghi*
**Symptoms:** Minute flecks appear on both leaf surfaces; circular-to-elongate cinnamon-brown, powdery, erumpent (bursting-through) pustules on both surfaces; pustules turn brownish-black as the crop matures; in severe cases, infection spreads to the leaf sheath and other plant parts.
**Alternate hosts:** *Oxalis europea, O. corniculata, O. stricta* (common wood-sorrel weeds) — the pathogen needs these to complete its life cycle before infecting maize.
**Favourable conditions:** cool, warm, moist weather (15-25°C).
**Management:**
- Remove alternate host weeds (Oxalis species) near the field
- Collect and destroy (burn or bury) crop remains after harvest
- Foliar spray: kresoxim-methyl 44.3% SC @ 1 ml/litre, OR tebuconazole @ 1 ml/litre, OR chlorothalonil/mancozeb @ 2 ml/litre — applied at 35 and 50 days after sowing (DAS)
**Source:** TNAU Agritech Portal — https://agritech.tnau.ac.in/crop_protection/maize_disease_new/maize_4.html

## Corn_Northern_Leaf_Blight
(TNAU catalogs this as "Leaf Blight" — matches Northern Leaf Blight / Turcicum Leaf Blight, same disease)
**Causal organism:** *Exserohilum turcicum* (and *Helminthosporium maydis*, per TNAU's listing)
**Symptoms:** Long, cigar-shaped, grey-green to tan lesions on lower leaves first; lesions are slender/oblong, tapering at the ends, 1-6 inches long; run parallel to leaf margins and coalesce to cover the entire leaf; spores produced on the underside of the leaf, giving a dusty black/green fuzz appearance below the lesions; affected leaves become greyish-green and brittle, resembling frost damage.
**Favourable conditions:** wet, humid, cool weather, typically later in the growing season.
**Management:**
- Burn or bury infected maize stubble after harvest
- Foliar spray: mancozeb or zineb @ 2-4 g/litre, OR propiconazole 25% EC @ 1 ml/litre — applied at 35 and 50 days after sowing (DAS)
**Source:** TNAU Agritech Portal — https://agritech.tnau.ac.in/crop_protection/maize_disease_new/maize_2.html

## Corn_Gray_Leaf_Spot
**Causal organism:** *Cercospora zeae-maydis*
**Symptoms:** Rectangular, narrow lesions bound by leaf veins, tan-to-gray in color, running parallel to the leaf veins; lesions can coalesce and cause significant blighting under heavy pressure; particularly damaging in warm (~27°C/80°F), high-humidity conditions (RH ≥90% for 12+ hours).
**Management:**
- Cultural: crop rotation and residue/stubble management (the pathogen survives in maize residue between seasons, so reduced-till/no-till/continuous maize cropping increases risk); use genetically resistant hybrids where available — considered the most economical long-term control
- Chemical: foliar fungicide applications with propiconazole or mancozeb have been shown to significantly reduce disease severity and improve yield in field trials — most effective when applied early, as disease severity reaches 2-3% of leaf area affected, and while lesions are still confined to the lowest 5 leaves
**Source:** consensus across multiple sources — PubMed/Plant Disease journal (https://pubmed.ncbi.nlm.nih.gov/30870945/, https://pubmed.ncbi.nlm.nih.gov/18943592/), Pioneer Seeds agronomy guide (https://www.pioneer.com/us/agronomy/gray_leaf_spot_cropfocus.html). **Not TNAU-sourced** — TNAU's maize disease page does not include Gray Leaf Spot among its 5 listed diseases (Downy Mildew, Turcicum Leaf Blight, Charcoal Rot, Common Rust, Aspergillus Rot). One source (a maize pathogen detection paper) does explicitly confirm the disease's presence in India among other countries, so the biology/treatment described here is still relevant to Indian conditions even though the specific sources are international.

## Corn_Healthy
No treatment needed — app should return a positive/no-action message when this class is predicted.

---

## Sourcing summary for this batch

- **Common Rust, Northern Leaf Blight:** fully TNAU-sourced, with real Indian-context details (alternate host weeds specific to the region, DAS-based spray timing consistent with Indian cropping calendars).
- **Gray Leaf Spot:** not on TNAU's maize page at all — sourced from international plant pathology literature instead. This is a genuine, disclosed gap consistent with the project's earlier-established convention of flagging rather than hiding sourcing limitations. Worth noting: this is also the exact class your trained model itself is weakest on for corn (F1 0.946, lowest of the 4 corn classes) — though still a strong score overall, it's a nice (if coincidental) alignment between "less-documented in Indian sources" and "harder for the model," worth a passing mention in your report if you want to draw that connection.

---

## Running total across all batches so far

19 of 30 classes complete: Tomato (10), Chili (2), Potato (3), Corn (4).
Remaining: Rice (4), Sugarcane (3), Cotton (4) — 11 classes left across 3 crop groups.
