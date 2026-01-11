from fastapi import APIRouter, HTTPException, Depends, Query
from app.schemas.insights import TrendsResponse, WeeklyInsightsResponse
from app.services.llm_service import generate_weekly_insights
from app.db.database import get_db
import aiosqlite
import json

router = APIRouter()

@router.get("/trends", response_model=TrendsResponse)
async def get_trends(
    session_id: str = Query(..., description="Session ID"),
    db: aiosqlite.Connection = Depends(get_db)
):
    """Get theme and emotion trends for a session"""
    
    # Verify session exists
    async with db.execute(
        "SELECT id FROM sessions WHERE id = ?", (session_id,)
    ) as cursor:
        session = await cursor.fetchone()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
    
    # Get all entry analyses
    async with db.execute(
        """
        SELECT themes_json, emotions_json
        FROM entry_analysis ea
        JOIN journal_entries je ON ea.entry_id = je.id
        WHERE je.session_id = ?
        """,
        (session_id,)
    ) as cursor:
        analyses = await cursor.fetchall()
    
    # Aggregate themes and emotions
    theme_counts: dict = {}
    emotion_counts: dict = {}
    
    for row in analyses:
        try:
            themes = json.loads(row[0]) if row[0] else []
            emotions = json.loads(row[1]) if row[1] else []
            
            for theme in themes:
                theme_counts[theme] = theme_counts.get(theme, 0) + 1
            
            for emotion in emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        except json.JSONDecodeError:
            continue
    
    # Get entry count and streak
    async with db.execute(
        "SELECT COUNT(*) FROM journal_entries WHERE session_id = ?",
        (session_id,)
    ) as cursor:
        entry_count = (await cursor.fetchone())[0]
    
    async with db.execute(
        "SELECT COUNT(DISTINCT day) FROM streak_days WHERE session_id = ?",
        (session_id,)
    ) as cursor:
        streak_row = await cursor.fetchone()
        streak_days = streak_row[0] if streak_row else 0
    
    return TrendsResponse(
        theme_counts=theme_counts,
        emotion_counts=emotion_counts,
        entry_count=entry_count,
        streak_days=streak_days,
    )

@router.get("/weekly", response_model=WeeklyInsightsResponse)
async def get_weekly_insights(
    session_id: str = Query(..., description="Session ID"),
    db: aiosqlite.Connection = Depends(get_db)
):
    """Get weekly reflection and pattern insights"""
    
    # Verify session exists
    async with db.execute(
        "SELECT id FROM sessions WHERE id = ?", (session_id,)
    ) as cursor:
        session = await cursor.fetchone()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
    
    # Get entries from last week
    async with db.execute(
        """
        SELECT ea.patterns_reflection, ea.themes_json, ea.emotions_json
        FROM entry_analysis ea
        JOIN journal_entries je ON ea.entry_id = je.id
        WHERE je.session_id = ?
        AND je.created_at >= datetime('now', '-7 days')
        ORDER BY je.created_at DESC
        """,
        (session_id,)
    ) as cursor:
        entries = await cursor.fetchall()
    
    # Prepare entry data for LLM service
    entry_data = []
    for row in entries:
        try:
            themes = json.loads(row[1]) if row[1] else []
            emotions = json.loads(row[2]) if row[2] else []
            entry_data.append({
                "patterns_reflection": row[0],
                "themes": themes,
                "emotions": emotions,
            })
        except json.JSONDecodeError:
            continue
    
    # Generate weekly insights (mock for now)
    insights = generate_weekly_insights(session_id, entry_data)
    
    return insights
    # return WeeklyInsightsResponse(
    #     patterns_reflection=insights["patterns_reflection"],
    #     themes=insights["themes"],
    #     emotions_summary=insights["emotions_summary"],
    # )

