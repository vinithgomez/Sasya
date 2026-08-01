function UncertainCard({ result }) {
  return (
    <div className="rounded-xl border border-amber-200 bg-amber-50 p-5">
      <h2 className="text-sm font-semibold text-amber-800 mb-1">Couldn't identify this image</h2>
      <p className="text-sm text-amber-700">{result.message}</p>
    </div>
  )
}

export default UncertainCard
