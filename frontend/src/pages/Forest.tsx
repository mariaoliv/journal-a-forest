import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useSession } from '../contexts/SessionContext'
import { apiClient, Tree } from '../services/api'

const RARITY_COLORS = {
  common: 'bg-forest-200 text-forest-800',
  uncommon: 'bg-forest-300 text-forest-900',
  rare: 'bg-forest-400 text-white',
  epic: 'bg-forest-600 text-white',
  legendary: 'bg-gradient-forest text-white',
}

const RARITY_LABELS = {
  common: 'Common',
  uncommon: 'Uncommon',
  rare: 'Rare',
  epic: 'Epic',
  legendary: 'Legendary',
}

const TREE_EMOJIS: Record<string, string> = {
  oak: '🌳',
  birch: '🌲',
  pine: '🌲',
  maple: '🍁',
  cherry: '🌸',
  willow: '🌿',
  cedar: '🌲',
  default: '🌱',
}

export default function Forest() {
  const navigate = useNavigate()
  const { sessionId, isLoading } = useSession()
  const [trees, setTrees] = useState<Tree[]>([])
  const [streak, setStreak] = useState(0)
  const [isLoadingGarden, setIsLoadingGarden] = useState(true)

  useEffect(() => {
    if (!isLoading && sessionId) {
      loadGarden()
    }
  }, [sessionId, isLoading])

  const loadGarden = async () => {
    if (!sessionId) return

    try {
      setIsLoadingGarden(true)
      const response = await apiClient.getGarden(sessionId)
      setTrees(response.trees)
      setStreak(response.streak_days)
    } catch (error) {
      console.error('Failed to load garden:', error)
    } finally {
      setIsLoadingGarden(false)
    }
  }

  if (isLoading || isLoadingGarden) {
    return (
      <div className="min-h-screen gradient-earth flex items-center justify-center">
        <div className="text-forest-700">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen gradient-earth py-12 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-12 text-center">
          <h1 className="text-5xl font-light text-forest-900 mb-4 tracking-tight">Your Forest</h1>
          <div className="inline-block px-6 py-3 bg-white/70 backdrop-blur-sm rounded-full border border-forest-200/60 shadow-sm card-hover">
            <span className="text-2xl font-light text-forest-900">
              🔥 <span className="font-normal">{streak}</span> day streak
            </span>
          </div>
        </div>

        {/* Trees Grid */}
        {trees.length === 0 ? (
          <div className="text-center py-16">
            <p className="text-xl text-forest-700 mb-4">No trees yet</p>
            <p className="text-forest-600 mb-8">Start journaling to plant your first tree!</p>
            <button
              onClick={() => navigate('/main')}
              className="px-8 py-3 bg-forest-600 hover:bg-forest-700 text-white rounded-full font-normal transition-all duration-300 ease-out shadow-lg hover:shadow-xl hover:scale-105 active:scale-100"
            >
              Write Your First Entry
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-12">
            {trees.map((tree) => {
              const emoji = TREE_EMOJIS[tree.type.toLowerCase()] || TREE_EMOJIS.default
              return (
                <div
                  key={tree.entry_id}
                  className="relative p-6 bg-gradient-to-br from-white/80 to-cream-50/40 backdrop-blur-sm rounded-2xl border border-forest-200/70 shadow-lg card-hover overflow-hidden group"
                >
                  <div className="absolute top-2 right-2 text-sm opacity-0 group-hover:opacity-40 transition-all duration-500 transform rotate-12 group-hover:-rotate-12">🍃</div>
                  <div className="text-7xl text-center mb-4 transition-all duration-500 group-hover:scale-125 group-hover:rotate-6">{emoji}</div>
                  <h3 className="text-lg font-normal text-forest-900 text-center mb-2 group-hover:text-forest-950 transition-colors duration-500">
                    {tree.display_name}
                  </h3>
                  <div className="text-center">
                    <span
                      className={`inline-block px-3 py-1.5 text-xs font-normal rounded-full transition-all duration-500 group-hover:scale-110 ${RARITY_COLORS[tree.rarity]}`}
                    >
                      {RARITY_LABELS[tree.rarity]}
                    </span>
                  </div>
                  <div className="mt-4 text-center">
                    <p className="text-sm text-forest-600 flex items-center justify-center gap-1">
                      <span className="text-xs">🌿</span>
                      {new Date(tree.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              )
            })}
          </div>
        )}

        {/* Navigation */}
        <div className="flex justify-center gap-4">
          <button
            onClick={() => navigate('/main')}
            className="px-6 py-2 text-forest-700 hover:text-forest-900 font-medium"
          >
            Back to Journal
          </button>
          <button
            onClick={() => navigate('/settings')}
            className="px-6 py-2 text-forest-700 hover:text-forest-900 font-medium"
          >
            Settings
          </button>
        </div>
      </div>
    </div>
  )
}

