import ConfidenceBar from '../components/ConfidenceBar'
import { overallMetrics, perClassResults } from '../data/modelResults'

function StatTile({ label, value }) {
  return (
    <div className="rounded-xl border border-stone-200 bg-white p-5 text-center shadow-sm">
      <p className="text-3xl font-semibold text-green-800 tabular-nums">{value}</p>
      <p className="mt-1 text-sm text-stone-500">{label}</p>
    </div>
  )
}

function cropOf(className) {
  return className.split('_')[0]
}

function Model() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-12 space-y-12">
      <section>
        <h1 className="text-2xl font-semibold text-stone-900 mb-2">Model</h1>
        <p className="text-stone-600 leading-relaxed">
          Sasya classifies plant diseases using <strong>EfficientNet-B0</strong>, fine-tuned via
          transfer learning from ImageNet weights. It's a single-label image classifier (not
          object detection) — one photo in, one of 30 disease/healthy classes out, spanning the 7
          supported crops: tomato, chili, potato, corn, rice, sugarcane, and cotton.
        </p>
      </section>

      <section>
        <h2 className="text-lg font-semibold text-stone-900 mb-4">Benchmark Results</h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <StatTile label="Overall Accuracy" value={`${(overallMetrics.accuracy * 100).toFixed(1)}%`} />
          <StatTile label="Macro F1" value={overallMetrics.macroF1.toFixed(3)} />
          <StatTile label="Weighted F1" value={overallMetrics.weightedF1.toFixed(3)} />
        </div>
        <p className="mt-3 text-xs text-stone-400">
          Trained for 15 epochs on GPU, all 30 classes, the full ~32.7k-image dataset (80/20
          stratified split, class-weighted loss, extra augmentation for underrepresented classes).
        </p>
      </section>

      <section>
        <h2 className="text-lg font-semibold text-stone-900 mb-4">Per-Class Results</h2>
        <div className="rounded-xl border border-stone-200 bg-white shadow-sm overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-stone-200 text-left text-xs uppercase tracking-wide text-stone-400">
                <th className="px-4 py-3 font-semibold">Crop</th>
                <th className="px-4 py-3 font-semibold">Class</th>
                <th className="px-4 py-3 font-semibold text-right">Precision</th>
                <th className="px-4 py-3 font-semibold text-right">Recall</th>
                <th className="px-4 py-3 font-semibold">F1</th>
                <th className="px-4 py-3 font-semibold text-right">Support</th>
              </tr>
            </thead>
            <tbody>
              {perClassResults.map((row) => (
                <tr key={row.class} className="border-b border-stone-100 last:border-0">
                  <td className="px-4 py-2.5 text-stone-400">{cropOf(row.class)}</td>
                  <td className="px-4 py-2.5 text-stone-800 font-medium">
                    {row.class.replaceAll('_', ' ')}
                  </td>
                  <td className="px-4 py-2.5 text-right text-stone-600 tabular-nums">
                    {row.precision.toFixed(3)}
                  </td>
                  <td className="px-4 py-2.5 text-right text-stone-600 tabular-nums">
                    {row.recall.toFixed(3)}
                  </td>
                  <td className="px-4 py-2.5">
                    <div className="flex items-center gap-2">
                      <ConfidenceBar value={row.f1} className="w-16" />
                      <span className="text-stone-600 tabular-nums text-xs">{row.f1.toFixed(3)}</span>
                    </div>
                  </td>
                  <td className="px-4 py-2.5 text-right text-stone-500 tabular-nums">{row.support}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section>
        <h2 className="text-lg font-semibold text-stone-900 mb-4">Known Limitations</h2>
        <div className="space-y-4">
          <div className="rounded-xl border border-amber-200 bg-amber-50 p-5">
            <h3 className="font-semibold text-amber-900 mb-2">Rice Brown Spot / Leaf Blast confusion</h3>
            <p className="text-sm text-amber-800 leading-relaxed">
              Every class hits F1 ≥ 0.93 except three Rice classes: Rice_Brown_Spot (F1 0.811) and
              Rice_Leaf_Blast (F1 0.856, missing ~20% of true blast cases), with Rice_Healthy also
              mildly affected. Confusion-matrix analysis shows this is a three-way cluster between
              these three classes — not a clean two-way mix-up — and Rice_Neck_Blast is completely
              unaffected (F1 1.000), so this isn't "Rice is hard" in general. The likely cause is
              under-detection of subtle early-stage lesions rather than pure disease-vs-disease
              visual similarity, though both effects are probably present.
            </p>
          </div>

          <div className="rounded-xl border border-amber-200 bg-amber-50 p-5">
            <h3 className="font-semibold text-amber-900 mb-2">Out-of-scope crop species</h3>
            <p className="text-sm text-amber-800 leading-relaxed">
              Given a real leaf photo from a crop species outside the 7 supported ones (e.g. pear
              or apple), the model does not express uncertainty — it confidently misclassifies the
              photo as one of its 30 trained classes, since it has no concept of "species outside
              my training set." This is different from the out-of-distribution safeguard for
              non-plant images: a confidence/entropy threshold can't fix it, because the model
              isn't uncertain here, it's confidently wrong. The current mitigation is UI copy only
              (the upload page states which 7 crops are supported) — a real fix would need a
              dedicated species-identification step before disease classification.
            </p>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Model
