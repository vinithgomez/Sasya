// Results only ever reach this bar once they've cleared the backend's OOD
// confidence gate (CONFIDENCE_THRESHOLD, currently 0.80) -- anything below
// that is intercepted and shown as the separate "uncertain" card instead.
// So there's no low/medium-confidence case to color-code here: every value
// this bar ever renders represents a confidently-identified result.
function ConfidenceBar({ value, className = '' }) {
  const pct = Math.round(value * 100)

  return (
    <div
      className={`h-2 rounded-full bg-stone-200 overflow-hidden ${className}`}
      role="progressbar"
      aria-valuenow={pct}
      aria-valuemin={0}
      aria-valuemax={100}
    >
      <div className="h-full bg-green-600 rounded-full" style={{ width: `${pct}%` }} />
    </div>
  )
}

export default ConfidenceBar
