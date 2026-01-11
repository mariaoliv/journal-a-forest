import { useEffect, useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useSession } from '../contexts/SessionContext'
import { apiClient, Prompt, Thread, EntryResponse } from '../services/api'

export default function Main() {
  const navigate = useNavigate()
  const location = useLocation()
  const { sessionId, isLoading } = useSession()
  const [prompts, setPrompts] = useState<Prompt[]>([])
  const [threads, setThreads] = useState<Thread[]>([])
  const [patternsReflection, setPatternsReflection] = useState<string | null>(null)
  const [isLoadingPrompts, setIsLoadingPrompts] = useState(true)
  const [numEntries, setNumEntries] = useState(0)

  useEffect(() => {
    if (!isLoading && sessionId) {
      loadPrompts()
    }
  }, [sessionId, isLoading])

  useEffect(() => {
    // Check if we have an entry response from navigation
    if (location.state?.entryResponse) {
      const entryResponse: EntryResponse = location.state.entryResponse
      if (entryResponse.patterns_reflection) {
        setPatternsReflection(entryResponse.patterns_reflection)
      }
      // Clear location state
      navigate(location.pathname, { replace: true, state: {} })
      // Reload prompts to get new ones
      if (sessionId) {
        setTimeout(() => loadPrompts(), 100)
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.state, navigate])

  const loadPrompts = async () => {
    if (!sessionId) return
    
    try {
      setIsLoadingPrompts(true)
      const nEntries = await apiClient.getNumEntries(sessionId)
      setNumEntries(nEntries.num_entries)
      const response = await apiClient.getTodayPrompts(sessionId)
      setPrompts(response.prompts)
      setThreads(response.active_threads)
    } catch (error) {
      console.error('Failed to load prompts:', error)
    } finally {
      setIsLoadingPrompts(false)
    }
  }

  const handlePromptSelect = (promptId: string) => {
    navigate(`/journaling/${promptId}`)
  }

  const handleNewEntry = () => {
    navigate('/journaling')
  }

  if (isLoading || isLoadingPrompts) {
    return (
      <div className="min-h-screen gradient-earth flex items-center justify-center">
        <div className="text-forest-700">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen gradient-earth py-12 px-4">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="mb-12 flex justify-between items-start">
          <div>
            <h1 className="text-4xl font-light text-forest-900 mb-2 tracking-tight">
              Your journal
            </h1>
            <p className="text-lg text-forest-600 font-light">Choose a prompt or write freely</p>
          </div>
          <button
            onClick={handleNewEntry}
            className="px-6 py-3 bg-forest-600 hover:bg-forest-700 text-white rounded-full font-normal transition-all duration-300 ease-out shadow-lg hover:shadow-xl hover:scale-105 active:scale-100"
          >
            New Entry
          </button>
        </div>

        {/* Patterns Section */}
        {patternsReflection && (
          <div className="mb-12 p-6 bg-gradient-to-br from-white/75 to-cream-50/50 backdrop-blur-sm rounded-2xl border border-forest-200/70 shadow-md card-hover relative overflow-hidden">
            <div className="absolute top-3 right-3 text-xl opacity-25 animate-pulse">🌿</div>
            <h2 className="text-xl font-normal text-forest-900 mb-3 relative flex items-center gap-2">
              <span className="text-lg">🍃</span>
              Patterns I'm noticing
            </h2>
            <p className="text-forest-700 leading-relaxed relative pl-6 border-l-2 border-forest-200/40">{patternsReflection}</p>
          </div>
        )}

        {/* Active Threads */}
        {threads.length > 0 && (
          <div className="mb-12">
            <h2 className="text-2xl font-light text-forest-900 mb-6 tracking-tight">Unfinished threads</h2>
            <div className="space-y-3">
              {threads.map((thread) => (
                <div
                  key={thread.id}
                  onClick={() => navigate(`/journaling?thread=${thread.id}`)}
                  className="p-5 bg-gradient-to-br from-white/75 to-cream-50/40 backdrop-blur-sm rounded-xl border border-forest-200/70 hover:border-forest-300 cursor-pointer card-hover shadow-md relative overflow-hidden group"
                >
                  <div className="absolute top-2 right-2 text-sm opacity-0 group-hover:opacity-40 transition-all duration-500 transform -rotate-12 group-hover:rotate-12">🍃</div>
                  <p className="text-forest-800 relative font-light">{thread.thread}</p>
                  <p className="text-sm text-forest-500 mt-3 relative flex items-center gap-1">
                    <span className="text-xs">🌿</span>
                    {new Date(thread.updated_at).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Prompts Grid */}
        <div className="mb-12">
          <h2 className="text-2xl font-light text-forest-900 mb-6 tracking-tight">Today's prompts</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {prompts.map((prompt) => (
              <button
                key={prompt.id}
                onClick={() => handlePromptSelect(prompt.id)}
                className="p-6 bg-gradient-to-br from-white/80 to-cream-50/40 backdrop-blur-sm rounded-xl border border-forest-200/70 hover:border-forest-300 text-left card-hover shadow-md relative overflow-hidden group"
              >
                <div className="absolute top-3 right-3 text-base opacity-0 group-hover:opacity-30 transition-all duration-500 transform rotate-12 group-hover:rotate-0">🌱</div>
                <p className="text-forest-800 text-lg leading-relaxed group-hover:text-forest-900 relative transition-colors duration-500 font-light">
                  {prompt.text}
                </p>
                {prompt.category && (
                  <span className="inline-block mt-4 px-3 py-1.5 text-xs font-normal text-forest-600 bg-forest-100/90 rounded-full relative group-hover:bg-forest-200/90 transition-colors duration-500">
                    {prompt.category}
                  </span>
                )}
              </button>
            ))}
          </div>
        </div>

        {/* Navigation */}
        <div className="flex justify-center gap-4">
          <button
            onClick={() => navigate('/forest')}
            className="px-6 py-2 text-forest-700 hover:text-forest-900 font-medium"
          >
            View Forest
          </button>
          <button
            onClick={() => navigate('/settings')}
            className="px-6 py-2 text-forest-700 hover:text-forest-900 font-medium"
          >
            Settings
          </button>
          <button
            onClick={() => navigate('/insights')}
            className="px-6 py-2 text-forest-700 hover:text-forest-900 font-medium"
            disabled={numEntries === 0 || numEntries % 7 !== 0}
          >
            Generate Weekly Insights
          </button>
        </div>
      </div>
    </div>
  )
}

