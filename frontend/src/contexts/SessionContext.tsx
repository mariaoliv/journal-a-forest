/* @refresh reset */
import { createContext, useContext, useState, useEffect, ReactNode, useCallback } from 'react'
import { apiClient } from '../services/api'

interface SessionContextType {
  sessionId: string | null
  isLoading: boolean
  ensureSession: () => Promise<string>
}

const SessionContext = createContext<SessionContextType | undefined>(undefined)

export function SessionProvider({ children }: { children: ReactNode }) {
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const ensureSession = useCallback(async (): Promise<string> => {
    let id = localStorage.getItem('session_id')
    
    if (!id) {
      try {
        const response = await apiClient.createSession()
        id = response.session_id
        localStorage.setItem('session_id', id)
        setSessionId(id)
      } catch (error) {
        console.error('Failed to create session:', error)
        setIsLoading(false)
        throw error // Re-throw so caller can handle it
      }
    } else {
      setSessionId(id)
    }
    
    setIsLoading(false)
    return id
  }, [])

  useEffect(() => {
    ensureSession().catch((error) => {
      console.error('Error in ensureSession:', error)
      setIsLoading(false) // Always set loading to false, even on error
    })
  }, [ensureSession])

  return (
    <SessionContext.Provider value={{ sessionId, isLoading, ensureSession }}>
      {children}
    </SessionContext.Provider>
  )
}

export function useSession() {
  const context = useContext(SessionContext)
  if (context === undefined) {
    throw new Error('useSession must be used within a SessionProvider')
  }
  return context
}

