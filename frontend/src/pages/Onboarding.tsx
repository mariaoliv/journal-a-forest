import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useSession } from '../contexts/SessionContext'
import { apiClient } from '../services/api'

export default function Onboarding() {
  const navigate = useNavigate()
  const { sessionId, ensureSession } = useSession()
  const [brainDump, setBrainDump] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!brainDump.trim()) {
      setError('Please share something about yourself')
      return
    }

    setIsSubmitting(true)
    setError(null)

    try {
      // Ensure we have a session ID before submitting
      let currentSessionId = sessionId
      if (!currentSessionId) {
        // Check localStorage first (in case context hasn't updated yet)
        currentSessionId = localStorage.getItem('session_id')
        if (!currentSessionId) {
          // Create new session - this will throw if it fails
          currentSessionId = await ensureSession()
        }
      }

      await apiClient.submitOnboarding({
        session_id: currentSessionId,
        brain_dump: brainDump.trim(),
      })
      
      // Navigate to main page - the main page will load prompts via API
      navigate('/main')
    } catch (err) {
      console.error('Onboarding submission failed:', err)
      let errorMessage = 'Failed to submit. Please try again.'
      if (err instanceof Error) {
        errorMessage = err.message || errorMessage
      } else if (typeof err === 'object' && err !== null && 'response' in err) {
        // Handle axios errors
        const axiosError = err as { response?: { data?: { detail?: string } } }
        errorMessage = axiosError.response?.data?.detail || errorMessage
      }
      setError(errorMessage)
      setIsSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen gradient-earth py-16 px-4">
      <div className="max-w-3xl mx-auto">
        <div className="mb-12 text-center relative">
          <div className="absolute top-0 left-1/2 transform -translate-x-1/2 text-4xl opacity-10 animate-float">🌿</div>
          <h1 className="text-4xl md:text-5xl font-light text-forest-900 mb-4 tracking-tight relative">
            Welcome to your forest
          </h1>
          <p className="text-xl text-forest-700 font-light">
            Let's start by getting to know you a little
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="brain-dump" className="block text-lg font-medium text-forest-800 mb-3">
              Share whatever comes to mind
            </label>
            <textarea
              id="brain-dump"
              value={brainDump}
              onChange={(e) => setBrainDump(e.target.value)}
              placeholder="What's on your mind? What are you feeling? What are you working through? There's no wrong answer here..."
              className="w-full min-h-[300px] px-6 py-4 border border-forest-200/60 rounded-xl focus:border-forest-300 focus:outline-none focus:ring-2 focus:ring-forest-200/30 resize-none text-forest-900 bg-white/90 placeholder-forest-400/60 text-lg leading-relaxed transition-all duration-300"
            />
          </div>

          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-8 py-3 bg-forest-600 hover:bg-forest-700 disabled:bg-forest-400 text-white rounded-full text-lg font-normal transition-all duration-300 ease-out shadow-lg hover:shadow-xl hover:scale-105 active:scale-100 disabled:cursor-not-allowed disabled:hover:scale-100"
            >
              {isSubmitting ? 'Processing...' : 'Continue'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

