import { useNavigate } from 'react-router-dom'
import { useSession } from '../contexts/SessionContext'
import { useEffect } from 'react'

export default function Landing() {
  const navigate = useNavigate()
  const { sessionId, isLoading, ensureSession } = useSession()

  const handleGetStarted = async () => {
    try {
      await ensureSession()
      navigate('/onboarding')
    } catch (error) {
      console.error('Failed to create session:', error)
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center gradient-earth">
        <div className="text-forest-700">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen gradient-earth flex items-center justify-center px-4 relative overflow-hidden">
      {/* Subtle decorative elements */}
      <div className="absolute top-20 left-10 text-5xl opacity-15 rotate-12 animate-float">🌿</div>
      <div className="absolute bottom-20 right-10 text-4xl opacity-15 -rotate-12 animate-float" style={{ animationDelay: '1s' }}>🍃</div>
      <div className="absolute top-1/2 right-20 text-3xl opacity-15 rotate-45 animate-float" style={{ animationDelay: '2s' }}>🌱</div>
      <div className="absolute top-1/3 left-20 text-3xl opacity-15 -rotate-12 animate-float" style={{ animationDelay: '0.5s' }}>🍂</div>
      
      <div className="max-w-2xl w-full text-center space-y-8 py-16 relative z-10">
        <div className="inline-block mb-2 text-4xl opacity-20">🌲</div>
        <h1 className="text-5xl md:text-6xl font-light text-forest-900 leading-tight mb-2 tracking-tight">
          Journal a Forest
        </h1>
        <p className="text-xl md:text-2xl text-forest-700 font-light leading-relaxed">
          Journaling doesn't have to be intimidating.
        </p>
        <p className="text-lg text-forest-600 mt-8 max-w-lg mx-auto leading-relaxed font-light">
          Plant a tree with every entry. Watch your thoughts grow into a forest of self-discovery.
        </p>
        <button
          onClick={handleGetStarted}
          className="mt-12 px-8 py-4 bg-gradient-to-r from-forest-600 to-forest-700 hover:from-forest-700 hover:to-forest-800 text-white rounded-full text-lg font-normal transition-all duration-500 ease-out shadow-xl hover:shadow-2xl hover:scale-110 active:scale-100 transform"
        >
          Start Journaling
        </button>
      </div>
    </div>
  )
}

