import { useState } from 'react'
import UploadForm from '../components/UploadForm'
import ResultCard from '../components/ResultCard'
import HealthyCard from '../components/HealthyCard'
import UncertainCard from '../components/UncertainCard'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function Home() {
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
      if (!res.ok) {
        let message = `Request failed (${res.status})`
        try {
          const errorData = await res.json()
          if (errorData?.detail) message = errorData.detail
        } catch {
          // response body wasn't JSON -- keep the generic message
        }
        throw new Error(message)
      }
      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const hasResult = Boolean(result || error)

  return (
    <div className="px-4 py-8 sm:py-12">
      <div className="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-[380px_1fr] gap-8 lg:items-start">
        {/* Left: upload form -- pinned in view on large screens while the page scrolls past the result */}
        <div className="lg:sticky lg:top-20 lg:self-start">
          <h1 className="text-2xl font-semibold text-stone-900 mb-1">Plant Disease Detection</h1>
          <p className="text-sm text-stone-500 mb-1">
            Upload a photo of a crop leaf to check for disease or pests.
          </p>
          <p className="text-xs text-stone-400 mb-8">
            Supports: Tomato, Chili, Potato, Corn, Rice, Sugarcane, Cotton
          </p>

          <UploadForm
            previewUrl={previewUrl}
            onFileChange={handleFileChange}
            onAnalyze={handleAnalyze}
            canAnalyze={!!file}
            loading={loading}
          />

          {error && <p className="mt-4 text-sm text-red-600">{error}</p>}
        </div>

        {/* Right: result -- flows with the page, whole-page scroll reveals it */}
        <div>
          {!hasResult && (
            <div className="min-h-[200px] sm:min-h-[280px] flex items-center justify-center rounded-xl border border-dashed border-stone-300 text-sm text-stone-400 px-4 text-center">
              Upload an image and click Analyze to see results here.
            </div>
          )}

          {result && result.status === 'uncertain' && <UncertainCard result={result} />}
          {result && result.status === 'ok' && result.is_healthy && <HealthyCard result={result} />}
          {result && result.status === 'ok' && !result.is_healthy && <ResultCard result={result} />}
        </div>
      </div>
    </div>
  )
}

export default Home
