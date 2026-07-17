import { useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [file, setFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    const selected = e.target.files?.[0]
    if (!selected) return
    setFile(selected)
    setPreviewUrl(URL.createObjectURL(selected))
    setResult(null)
    setError(null)
  }

  const handleAnalyze = async () => {
    if (!file) return
    setLoading(true)
    setError(null)
    try {
      const formData = new FormData()
      formData.append('file', file)
      const res = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        body: formData,
      })
      if (!res.ok) throw new Error(`Request failed (${res.status})`)
      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-svh bg-gray-50 flex flex-col items-center px-4 py-12">
      <div className="w-full max-w-md">
        <h1 className="text-2xl font-semibold text-gray-900 mb-1">
          Plant Disease Detection
        </h1>
        <p className="text-sm text-gray-500 mb-8">
          Upload a photo of a crop leaf to check for disease or pests.
        </p>

        <label className="block cursor-pointer rounded-lg border-2 border-dashed border-gray-300 bg-white p-6 text-center hover:border-green-500 transition-colors">
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="hidden"
          />
          {previewUrl ? (
            <img
              src={previewUrl}
              alt="Selected leaf preview"
              className="mx-auto max-h-64 rounded-md object-contain"
            />
          ) : (
            <span className="text-sm text-gray-500">
              Click to choose an image
            </span>
          )}
        </label>

        <button
          type="button"
          onClick={handleAnalyze}
          disabled={!file || loading}
          className="mt-4 w-full rounded-md bg-green-600 px-4 py-2 text-white font-medium hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>

        {error && (
          <p className="mt-4 text-sm text-red-600">{error}</p>
        )}

        {result && (
          <div className="mt-6 rounded-lg border border-gray-200 bg-white p-4">
            <h2 className="text-sm font-medium text-gray-500 mb-2">Result</h2>
            <p className="text-lg font-semibold text-gray-900">
              {result.class}
            </p>
            <p className="text-sm text-gray-500">
              Confidence: {(result.confidence * 100).toFixed(1)}%
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
