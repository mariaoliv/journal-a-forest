import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useSession } from '../contexts/SessionContext'
import { apiClient } from '../services/api'

export default function Settings() {
  const navigate = useNavigate()
  const { sessionId } = useSession()
  const [showConfirmDelete, setShowConfirmDelete] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleDeleteAll = async () => {
    if (!sessionId) {
      setError('Session not found')
      return
    }

    setIsDeleting(true)
    setError(null)

    try {
      await apiClient.deleteMemories(sessionId)
      
      // Clear local storage and redirect
      localStorage.removeItem('session_id')
      navigate('/')
    } catch (err) {
      console.error('Failed to delete memories:', err)
      setError('Failed to delete. Please try again.')
      setIsDeleting(false)
    }
  }

  return (
    <div className="min-h-screen gradient-earth py-12 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="mb-12">
          <button
            onClick={() => navigate('/main')}
            className="text-forest-600 hover:text-forest-900 mb-4 inline-flex items-center"
          >
            ← Back
          </button>
          <h1 className="text-4xl font-light text-forest-900 tracking-tight">Settings</h1>
        </div>

        {/* Danger Zone */}
        <div className="p-8 bg-white/70 backdrop-blur-sm rounded-2xl border-2 border-red-200 shadow-md card-hover">
          <h2 className="text-2xl font-medium text-red-900 mb-4">Danger Zone</h2>
          <p className="text-forest-700 mb-6 leading-relaxed">
            Delete all your journal entries, trees, and memories. This action cannot be undone.
          </p>

          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}

          {!showConfirmDelete ? (
            <button
              onClick={() => setShowConfirmDelete(true)}
              className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors shadow-lg hover:shadow-xl"
            >
              Delete All Memories
            </button>
          ) : (
            <div className="space-y-4">
              <p className="text-red-800 font-medium">
                Are you sure? Type "DELETE" to confirm:
              </p>
              <div className="flex gap-4">
                <button
                  onClick={handleDeleteAll}
                  disabled={isDeleting}
                  className="px-6 py-3 bg-red-600 hover:bg-red-700 disabled:bg-red-400 text-white rounded-lg font-medium transition-colors shadow-lg hover:shadow-xl disabled:cursor-not-allowed"
                >
                  {isDeleting ? 'Deleting...' : 'Confirm Delete'}
                </button>
                <button
                  onClick={() => {
                    setShowConfirmDelete(false)
                    setError(null)
                  }}
                  disabled={isDeleting}
                  className="px-6 py-3 bg-forest-200 hover:bg-forest-300 text-forest-800 rounded-lg font-medium transition-colors"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Info Section */}
        <div className="mt-12 p-6 bg-gradient-to-br from-white/75 to-cream-50/40 backdrop-blur-sm rounded-xl border border-forest-200/70 shadow-sm card-hover relative overflow-hidden">
          <div className="absolute top-2 right-2 text-lg opacity-20">🌿</div>
          <h3 className="text-lg font-medium text-forest-900 mb-3">About</h3>
          <p className="text-forest-700 leading-relaxed">
            Journal a Forest is a mindful journaling companion. Every entry plants a tree,
            helping you grow your forest of self-discovery.
          </p>
        </div>
      </div>
    </div>
  )
}

