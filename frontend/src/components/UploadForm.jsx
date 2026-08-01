function UploadForm({ previewUrl, onFileChange, onAnalyze, canAnalyze, loading }) {
  return (
    <div>
      <label className="block cursor-pointer rounded-lg border-2 border-dashed border-stone-300 bg-white p-6 text-center hover:border-green-500 transition-colors">
        <input type="file" accept="image/*" onChange={onFileChange} className="hidden" />
        {previewUrl ? (
          <img
            src={previewUrl}
            alt="Selected leaf preview"
            className="mx-auto max-h-64 rounded-md object-contain"
          />
        ) : (
          <span className="text-sm text-stone-500">Click to choose an image</span>
        )}
      </label>

      <button
        type="button"
        onClick={onAnalyze}
        disabled={!canAnalyze || loading}
        className="mt-4 w-full rounded-md bg-green-700 px-4 py-2 text-white font-medium hover:bg-green-800 disabled:bg-stone-300 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? (
          <span className="flex items-center justify-center gap-2">
            <span className="h-4 w-4 rounded-full border-2 border-white border-t-transparent animate-spin" />
            Analyzing...
          </span>
        ) : (
          'Analyze'
        )}
      </button>
    </div>
  )
}

export default UploadForm
