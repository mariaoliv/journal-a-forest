import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface SessionResponse {
  session_id: string
}

export interface OnboardingRequest {
  session_id: string
  brain_dump: string
}

export interface OnboardingResponse {
  starter_prompts: Prompt[]
  active_threads: Thread[]
  initial_tree: Tree
}

export interface Prompt {
  id: string
  text: string
  category?: string
}

export interface Thread {
  id: number
  thread: string
  status: 'active' | 'snoozed' | 'resolved'
  created_at: string
  updated_at: string
  last_seen_entry_id?: number
}

export interface Tree {
  entry_id: number
  session_id: string
  created_at: string
  type: string
  rarity: 'common' | 'uncommon' | 'rare' | 'epic' | 'legendary'
  display_name: string
}

export interface TodayPromptsResponse {
  prompts: Prompt[]
  active_threads: Thread[]
}

export interface EntryRequest {
  session_id: string
  prompt_id?: string
  text: string
}

export interface EntryResponse {
  entry_id: number
  memory_summary: string
  patterns_reflection: string
  follow_up_question: string
  themes: string[]
  emotions: string[]
  new_prompts: Prompt[]
  tree: Tree
  streak_updated: number
}

export interface NumEntries {
  num_entries: number
}

export interface GardenResponse {
  streak_days: number
  trees: Tree[]
}

export interface ThreadUpdateRequest {
  status: 'active' | 'snoozed' | 'resolved'
}

export interface TrendsResponse {
  theme_counts: Record<string, number>
  emotion_counts: Record<string, number>
  entry_count: number
  streak_days: number
}

export interface WeeklyInsightsResponse {
  patterns_reflection: string
  themes: string[]
  emotions_summary: Record<string, number>
}

export const apiClient = {
  async createSession(): Promise<SessionResponse> {
    const response = await client.post<SessionResponse>('/api/session')
    return response.data
  },

  async submitOnboarding(data: OnboardingRequest): Promise<OnboardingResponse> {
    const response = await client.post<OnboardingResponse>('/api/onboarding', data)
    return response.data
  },

  async getTodayPrompts(sessionId: string): Promise<TodayPromptsResponse> {
    const response = await client.get<TodayPromptsResponse>('/api/prompts/today', {
      params: { session_id: sessionId },
    })
    return response.data
  },

  async createEntry(data: EntryRequest): Promise<EntryResponse> {
    const response = await client.post<EntryResponse>('/api/entries', data)
    return response.data
  },

  async getNumEntries(sessionId: string): Promise<NumEntries> {
    const response = await client.get<NumEntries>('/api/num_entries', {
      params : { session_id : sessionId },
    })
    return response.data
  },

  async getGarden(sessionId: string): Promise<GardenResponse> {
    const response = await client.get<GardenResponse>('/api/garden', {
      params: { session_id: sessionId },
    })
    return response.data
  },

  async updateThread(threadId: number, data: ThreadUpdateRequest): Promise<void> {
    await client.post(`/api/threads/${threadId}`, data)
  },

  async getTrends(sessionId: string): Promise<TrendsResponse> {
    const response = await client.get<TrendsResponse>('/api/insights/trends', {
      params: { session_id: sessionId },
    })
    return response.data
  },

  async getWeeklyInsights(sessionId: string): Promise<WeeklyInsightsResponse> {
    const response = await client.get<WeeklyInsightsResponse>('/api/insights/weekly', {
      params: { session_id: sessionId },
    })
    return response.data
  },

  async deleteMemories(sessionId: string): Promise<void> {
    await client.delete('/api/memories', {
      params: { session_id: sessionId },
    })
  },
}

