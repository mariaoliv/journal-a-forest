import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useSession } from '../contexts/SessionContext'
import { apiClient, TrendsResponse, WeeklyInsightsResponse } from '../services/api'

export default function Insights() {
  const navigate = useNavigate()
  
  const { sessionId } = useSession()
  const [weeklyInsights, setWeeklyInsights] = useState<WeeklyInsightsResponse | null>(null)
  const [trends, setTrends] = useState<TrendsResponse | null>(null)

  useEffect(() => {
    if (sessionId) {
      // Load prompt details if needed
      loadWeeklyInsights(sessionId)
      loadTrends(sessionId)
    }
  }, [sessionId])

  const loadWeeklyInsights = async (sessionId: string) => {
    try {
        const response = await apiClient.getWeeklyInsights(sessionId)
        setWeeklyInsights(response)
    }
    catch(error) {
        console.error('Failed to get weekly insights: ', error)
    }
  }

  const loadTrends = async (sessionId: string) => {
    try {
        const weekly_trends = await apiClient.getTrends(sessionId)
        setTrends(weekly_trends)
    }
    catch(error) {
        console.error('Failed to get trends: ', error)
    }
  }

  return (
  <div className="min-h-screen gradient-earth py-12 px-4">
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <button
          onClick={() => navigate('/main')}
          className="text-forest-600 hover:text-forest-900 mb-4 inline-flex items-center gap-2"
        >
          <span className="text-lg">←</span>
          Back
        </button>

        <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-3">
          <div>
            <h1 className="text-4xl font-light text-forest-900 tracking-tight">
              Weekly Insights
            </h1>
            <p className="text-forest-700/80 mt-1">
              Your latest patterns + what’s been showing up most often.
            </p>
          </div>

          {/* Quick stats */}
          {trends && (
            <div className="flex gap-2">
              <div className="px-3 py-2 rounded-2xl bg-white/70 border border-forest-200/70 backdrop-blur-sm shadow-sm">
                <div className="text-xs text-forest-600">Entries</div>
                <div className="text-lg font-medium text-forest-900">{trends.entry_count}</div>
              </div>
              <div className="px-3 py-2 rounded-2xl bg-white/70 border border-forest-200/70 backdrop-blur-sm shadow-sm">
                <div className="text-xs text-forest-600">Streak</div>
                <div className="text-lg font-medium text-forest-900">{trends.streak_days} days</div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Content grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Reflection card */}
        <div className="p-6 bg-gradient-to-br from-white/75 to-cream-50/50 backdrop-blur-sm rounded-2xl border border-forest-200/70 shadow-md relative overflow-hidden">
          <div className="absolute top-4 right-4 text-2xl opacity-25">🌿</div>

          <h2 className="text-lg font-medium text-forest-900">Reflection</h2>
          <p className="text-sm text-forest-700/80 mt-1">
            A gentle read on your last week’s entries.
          </p>

          {!weeklyInsights ? (
            <div className="mt-5 rounded-xl border border-forest-200/60 bg-white/50 p-4 text-forest-700">
              <div className="text-sm">Loading reflection…</div>
            </div>
          ) : (
            <div className="mt-5 space-y-4">
              <div className="rounded-xl border border-forest-200/60 bg-white/50 p-4">
                <div className="text-xs uppercase tracking-wide text-forest-600">
                  Pattern snapshot
                </div>
                <div className="mt-2 text-forest-900 leading-relaxed whitespace-pre-wrap">
                  {weeklyInsights.patterns_reflection || (
                    <span className="text-forest-700/70">
                      No reflection available yet.
                    </span>
                  )}
                </div>
              </div>

              {/* Optional, non-repetitive: show detected themes as chips (not counts) */}
              {weeklyInsights.themes?.length > 0 && (
                <div className="rounded-xl border border-forest-200/60 bg-white/40 p-4">
                  <div className="text-xs uppercase tracking-wide text-forest-600">
                    Detected themes
                  </div>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {weeklyInsights.themes.slice(0, 10).map((t) => (
                      <span
                        key={t}
                        className="inline-flex items-center px-3 py-1 rounded-full bg-white/60 border border-forest-200/70 text-forest-900 text-sm"
                      >
                        {t}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Trends card */}
        <div className="p-6 bg-gradient-to-br from-white/75 to-cream-50/50 backdrop-blur-sm rounded-2xl border border-forest-200/70 shadow-md relative overflow-hidden">
          <div className="absolute top-4 right-4 text-2xl opacity-25">🍃</div>

          <h2 className="text-lg font-medium text-forest-900">Trends</h2>
          <p className="text-sm text-forest-700/80 mt-1">
            Top themes + emotions across your recent entries.
          </p>

          {!trends ? (
            <div className="mt-5 rounded-xl border border-forest-200/60 bg-white/50 p-4 text-forest-700">
              <div className="text-sm">Loading trends…</div>
            </div>
          ) : (
            <div className="mt-5 space-y-6">
              {/* Top themes as chips with counts */}
              <div>
                <div className="text-xs uppercase tracking-wide text-forest-600">
                  Top themes
                </div>

                {Object.keys(trends.theme_counts || {}).length === 0 ? (
                  <div className="mt-2 text-forest-700/70 text-sm">
                    No themes counted yet.
                  </div>
                ) : (
                  <div className="mt-3 flex flex-wrap gap-2">
                    {Object.entries(trends.theme_counts)
                      .sort((a, b) => b[1] - a[1])
                      .slice(0, 8)
                      .map(([theme, count]) => (
                        <span
                          key={theme}
                          className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/60 border border-forest-200/70 text-forest-900 text-sm"
                        >
                          <span className="capitalize">{theme}</span>
                          <span className="text-forest-600/80 text-xs">{count}</span>
                        </span>
                      ))}
                  </div>
                )}
              </div>

              {/* Emotions as simple bars */}
              <div>
                <div className="text-xs uppercase tracking-wide text-forest-600">
                  Top emotions
                </div>

                {Object.keys(trends.emotion_counts || {}).length === 0 ? (
                  <div className="mt-2 text-forest-700/70 text-sm">
                    No emotions counted yet.
                  </div>
                ) : (
                  <div className="mt-3 space-y-2">
                    {(() => {
                      const sorted = Object.entries(trends.emotion_counts).sort((a, b) => b[1] - a[1])
                      const max = sorted[0]?.[1] ?? 1
                      return sorted.slice(0, 6).map(([emotion, count]) => (
                        <div key={emotion} className="flex items-center gap-3">
                          <div className="w-24 text-sm text-forest-900 capitalize">
                            {emotion}
                          </div>
                          <div className="flex-1 h-2 rounded-full bg-white/40 border border-forest-200/60 overflow-hidden">
                            <div
                              className="h-full bg-forest-300/70"
                              style={{ width: `${Math.max(10, Math.round((count / max) * 100))}%` }}
                            />
                          </div>
                          <div className="w-8 text-sm text-forest-700">{count}</div>
                        </div>
                      ))
                    })()}
                  </div>
                )}
              </div>

              <div className="rounded-xl border border-forest-200/60 bg-white/40 p-4 text-sm text-forest-700">
                These trends update as you write—more entries = clearer signal.
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="mt-8 flex items-center justify-between">
        <button
          onClick={() => navigate('/main')}
          className="px-4 py-2 rounded-xl bg-white/70 border border-forest-200/70 text-forest-800 hover:text-forest-900 hover:bg-white/80 backdrop-blur-sm"
        >
          Back to journal
        </button>
      </div>
    </div>
  </div>
)

}

