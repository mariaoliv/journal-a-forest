import { useState, useEffect } from 'react'
import { useNavigate, useParams, useSearchParams } from 'react-router-dom'
import { useSession } from '../contexts/SessionContext'
import { apiClient, Prompt } from '../services/api'

export default function Journaling() {
  const navigate = useNavigate()
  const { promptId } = useParams<{ promptId?: string }>()
  const [searchParams] = useSearchParams()
  const threadId = searchParams.get('thread')
  
  const { sessionId } = useSession()
  const [prompt, setPrompt] = useState<Prompt | null>(null)
  const [entryText, setEntryText] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (promptId && sessionId) {
      // Load prompt details if needed
      loadPrompt(promptId)
    }
  }, [promptId, sessionId])

  const loadPrompt = async (id: string) => {
    try {
      const response = await apiClient.getTodayPrompts(sessionId!)
      const found = response.prompts.find((p) => p.id === id)
      if (found) {
        setPrompt(found)
      }
    } catch (error) {
      console.error('Failed to load prompt:', error)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!entryText.trim()) {
      setError('Please write something')
      return
    }

    if (!sessionId) {
      setError('Session not found. Please refresh.')
      return
    }

    setIsSubmitting(true)
    setError(null)

    try {
      const response = await apiClient.createEntry({
        session_id: sessionId,
        prompt_id: promptId,
        text: entryText.trim(),
      })

      // Show success and navigate
      navigate('/main', {
        state: {
          entryResponse: response,
          showPatterns: true,
        },
      })
    } catch (err) {
      console.error('Entry submission failed:', err)
      setError('Failed to save entry. Please try again.')
      setIsSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen gradient-earth py-12 px-4">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/main')}
            className="text-forest-600 hover:text-forest-900 mb-4 inline-flex items-center"
          >
            ← Back
          </button>
          <h1 className="text-4xl font-light text-forest-900 tracking-tight">New entry</h1>
        </div>

        {/* Prompt Display */}
        {prompt && (
          <div className="mb-8 p-6 bg-gradient-to-br from-white/75 to-cream-50/50 backdrop-blur-sm rounded-xl border border-forest-200/70 shadow-md relative overflow-hidden">
            <div className="absolute top-3 right-3 text-xl opacity-25">🌿</div>
            <p className="text-lg text-forest-800 leading-relaxed relative font-light pl-4 border-l-2 border-forest-200/50">{prompt.text}</p>
          </div>
        )}

        {/* Editor */}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="entry-text" className="block text-lg font-medium text-forest-800 mb-3">
              {prompt ? 'Write your response' : "What's on your mind?"}
            </label>
            <textarea
              id="entry-text"
              value={entryText}
              onChange={(e) => setEntryText(e.target.value)}
              placeholder={prompt ? 'Take your time...' : 'Write freely about anything that comes to mind...'}
              className="w-full min-h-[400px] px-6 py-4 border border-forest-200/60 rounded-xl focus:border-forest-300 focus:outline-none focus:ring-2 focus:ring-forest-200/30 resize-none text-forest-900 bg-white/90 placeholder-forest-400/60 text-lg leading-relaxed transition-all duration-300"
              autoFocus
            />
          </div>

          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}

          <div className="flex justify-end gap-4">
            <button
              type="button"
              onClick={() => navigate('/main')}
              className="px-6 py-3 text-forest-700 hover:text-forest-900 font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-8 py-3 bg-forest-600 hover:bg-forest-700 disabled:bg-forest-400 text-white rounded-full text-lg font-normal transition-all duration-300 ease-out shadow-lg hover:shadow-xl hover:scale-105 active:scale-100 disabled:cursor-not-allowed disabled:hover:scale-100"
            >
              {isSubmitting ? 'Saving...' : 'Save Entry'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

