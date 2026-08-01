function Section({ title, children }) {
  return (
    <section>
      <h2 className="text-lg font-semibold text-stone-900 mb-3">{title}</h2>
      <div className="text-stone-600 leading-relaxed space-y-3">{children}</div>
    </section>
  )
}

function About() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-12 space-y-12">
      <section>
        <h1 className="text-2xl font-semibold text-stone-900 mb-2">About Sasya</h1>
        <p className="text-stone-600 leading-relaxed">
          <em>Sasya</em> is Sanskrit for "plant/crop." The project grew out of an "AI for
          Low-Pesticide Agriculture" framing — using a trained classifier plus sourced treatment
          guidance to help identify crop disease early, so growers can act on it, rather than
          reaching for broad-spectrum pesticide as a default.
        </p>
      </section>

      <Section title="Why regional India, specifically">
        <p>
          Most publicly available plant disease datasets (PlantVillage included) skew toward
          crops and imaging conditions common in the US. Sasya instead targets 7 crops
          specifically significant to Indian agriculture — tomato, chili, potato, corn, rice,
          sugarcane, and cotton — spanning 30 disease/healthy classes.
        </p>
        <p>
          This matters beyond coverage: some included diseases, like Cotton Leaf Curl Virus, are
          documented as major, economically damaging diseases specific to the Indian
          subcontinent, and simply aren't present in generic global training sets.
        </p>
      </Section>

      <Section title="Dataset sourcing">
        <p>Three datasets were merged to cover the target crop list, since no single dataset covers all 7:</p>
        <ul className="list-disc list-inside space-y-1">
          <li><strong>PlantVillage</strong> — tomato, chili (bell pepper proxy), potato, corn</li>
          <li><strong>Five Crop Diseases Dataset</strong> — rice, sugarcane</li>
          <li><strong>Cotton Leaf Disease Dataset</strong> — cotton</li>
        </ul>
        <p>
          Class folder names across the three sources were reconciled into one unified naming
          scheme before training. Full sourcing details, licenses, and the complete class-mapping
          table are documented in the repo's <code className="text-sm bg-stone-100 px-1 py-0.5 rounded">data/README.md</code>.
        </p>
      </Section>

      <Section title="Treatment recommendation sourcing">
        <p>
          Every disease's causal organism, symptoms, and management guidance is sourced, not
          generated — sourced primarily from <strong>TNAU</strong> (Tamil Nadu Agricultural
          University) Agritech Portal, an Indian government agricultural university source that
          matches the project's regional-India focus.
        </p>
        <p>
          Where TNAU didn't have dedicated coverage for a class, that gap is explicitly flagged
          rather than silently filled in from a generic or US-centric source — a small number of
          classes (e.g. Tomato Leaf Mold, Tomato Target Spot, Corn Gray Leaf Spot) are sourced from
          international extension/research literature instead, and are marked as such wherever
          they appear.
        </p>
      </Section>

      <Section title="Tech stack">
        <ul className="list-disc list-inside space-y-1">
          <li><strong>Frontend</strong> — React, Vite, Tailwind CSS, React Router</li>
          <li><strong>Backend</strong> — FastAPI serving model inference</li>
          <li><strong>Model</strong> — EfficientNet-B0, fine-tuned via transfer learning (PyTorch / TorchVision)</li>
          <li><strong>Treatment layer</strong> — a sourced, rules-based lookup table (not LLM-generated)</li>
        </ul>
      </Section>
    </div>
  )
}

export default About
