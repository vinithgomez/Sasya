import ConfidenceBar from './ConfidenceBar'

function ResultCard({ result }) {
  const { class: predictedClass, confidence, treatment } = result
  const displayName = predictedClass.replaceAll('_', ' ')

  return (
    <div className="rounded-xl border border-stone-200 bg-white shadow-sm overflow-hidden">
      {/* 1. Class name + confidence bar */}
      <div className="p-5 border-b border-stone-100">
        <h2 className="text-xl font-semibold text-stone-900">{displayName}</h2>
        <div className="mt-3 flex items-center gap-3">
          <ConfidenceBar value={confidence} className="flex-1" />
          <span className="text-sm font-medium text-stone-600 tabular-nums">
            {(confidence * 100).toFixed(1)}%
          </span>
        </div>
      </div>

      {/* 2. Causal organism -- labeled row, not a paragraph */}
      {treatment?.causal_organism && (
        <div className="px-5 py-3 border-b border-stone-100 bg-amber-50/60 flex items-start gap-3">
          <span className="shrink-0 mt-0.5 inline-flex items-center rounded-full bg-amber-100 text-amber-800 px-2.5 py-1 text-xs font-semibold uppercase tracking-wide">
            Causal Organism
          </span>
          <span className="text-sm text-stone-700 italic">{treatment.causal_organism}</span>
        </div>
      )}

      {/* 3. Symptoms | Management -- two-column on desktop, stacked on mobile */}
      <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-stone-100">
        {treatment?.symptoms && (
          <div className="p-5">
            <h3 className="text-xs font-semibold uppercase tracking-wide text-stone-400 mb-2">
              Symptoms
            </h3>
            <p className="text-sm text-stone-700 leading-relaxed">{treatment.symptoms}</p>
          </div>
        )}

        {treatment?.management?.length > 0 && (
          <div className="p-5">
            <h3 className="text-xs font-semibold uppercase tracking-wide text-stone-400 mb-2">
              Management
            </h3>
            <ul className="text-sm text-stone-700 space-y-1.5 list-disc list-inside">
              {treatment.management.map((step, i) => (
                <li key={i}>{step}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* 4. Source -- de-emphasized but visible */}
      {treatment?.source && (
        <div className="px-5 py-3 bg-stone-50 border-t border-stone-100">
          <p className="text-xs text-stone-400">Source: {treatment.source}</p>
        </div>
      )}
    </div>
  )
}

export default ResultCard
