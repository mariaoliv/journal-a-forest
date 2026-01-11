from fastapi import APIRouter, HTTPException, Depends, Query
from app.schemas.prompts import TodayPromptsResponse
from app.services.llm_service import generate_prompts
from app.services.chroma_service import ChromaService
from app.db.database import get_db
import aiosqlite
from typing import Optional

router = APIRouter()
chroma_db = ChromaService()

@router.get("/today", response_model=TodayPromptsResponse)
async def get_today_prompts(
    session_id: str = Query(..., description="Session ID"),
    db: aiosqlite.Connection = Depends(get_db)
):
    """Get today's prompts and active threads for a session"""
    
    # Verify session exists
    async with db.execute(
        "SELECT id FROM sessions WHERE id = ?", (session_id,)
    ) as cursor:
        session = await cursor.fetchone()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
    
    # Get recent entries for context (for prompt generation)
    async with db.execute(
        """
        SELECT memory_summary, entry_id
        FROM entry_analysis ea
        JOIN journal_entries je ON ea.entry_id = je.id
        WHERE session_id = ?
        ORDER BY created_at DESC
        LIMIT 3
        """,
        (session_id,)
    ) as cursor:
        recent_entries = await cursor.fetchall()

    # Get active threads
    async with db.execute(
        """
        SELECT id, thread, status, created_at, updated_at, last_seen_entry_id
        FROM threads
        WHERE session_id = ? AND status = 'active'
        ORDER BY updated_at DESC
        LIMIT 3
        """,
        (session_id,)
    ) as cursor:
        thread_rows = await cursor.fetchall()
    
    active_threads = [
        {
            "id": row[0],
            "thread": row[1],
            "status": row[2],
            "created_at": row[3],
            "updated_at": row[4],
            "last_seen_entry_id": row[5],
        }
        for row in thread_rows
    ]

    summary = recent_entries[0][0]
    recent_summaries = [res[0] for res in recent_entries]
    recent_entry_ids = [res[1] for res in recent_entries]
    #query ChromaDB to get most similar entries to form session history
    similarity_search_results = chroma_db.search_similar(query=summary, session_id=session_id, exclude_entry_ids=recent_entry_ids, limit=5)

    session_history = {
        "recent_memories": recent_summaries,
        "relevant_memories": similarity_search_results,
        "active_threads": active_threads
    }

    #session_history = [{"summary": row[0]} for row in recent_entries]
    
    # Generate prompts (mock for now)
    prompt_data = generate_prompts("", session_history)
    
    prompts = [
        {
            "id": p["id"],
            "text": p["text"],
            "category": p.get("category"),
        }
        for p in prompt_data
    ]
    
    
    return TodayPromptsResponse(
        prompts=prompts,
        active_threads=active_threads,
    )

