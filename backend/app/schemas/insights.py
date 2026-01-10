from pydantic import BaseModel
from typing import Dict, List

class TrendsResponse(BaseModel):
    theme_counts: Dict[str, int]
    emotion_counts: Dict[str, int]
    entry_count: int
    streak_days: int

class WeeklyInsightsResponse(BaseModel):
    patterns_reflection: str
    themes: List[str]
    emotions_summary: Dict[str, int]

