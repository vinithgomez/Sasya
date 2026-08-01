import ConfidenceBar from './ConfidenceBar'

function HealthyCard({ result }) {
  const displayName = result.class.replaceAll('_', ' ')

  return (
    <div className="rounded-xl border border-green-200 bg-green-50 p-5">
      <h2 className="text-xl font-semibold text-green-900">{displayName}</h2>
      <div className="mt-3 flex items-center gap-3">
        <ConfidenceBar value={result.confidence} className="flex-1" />
        <span className="text-sm font-medium text-green-700 tabular-nums">
          {(result.confidence * 100).toFixed(1)}%
        </span>
      </div>
      <p className="mt-4 text-sm text-green-800">{result.treatment?.management?.[0]}</p>
    </div>
  )
}

export default HealthyCard
