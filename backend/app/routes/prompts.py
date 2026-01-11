from fastapi import APIRouter, HTTPException, Depends, Query
from app.schemas.prompts import TodayPromptsResponse
from app.services.llm_service import generate_prompts
from app.services.chroma_service import ChromaService
from app.db.database import get_db
import aiosqlite
import json
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
    
    async with db.execute(
        """
        SELECT COUNT(id) FROM journal_entries
        WHERE session_id = ?
        """,
        (session_id,)
    ) as cursor:
        num_entries = (await cursor.fetchone())[0]

    async with db.execute(
        """
        SELECT COUNT(*) FROM prompts
        WHERE session_id = ? AND source = ?
        """,
        (session_id, "generated")
    ) as cursor:
        num_generated_prompts = (await cursor.fetchone())[0]

    if num_entries == 0 or num_generated_prompts == 0:
        #use starter prompts
        async with db.execute(
        """
        SELECT prompts_json FROM prompts
        WHERE source = ? AND session_id = ?
        """, 
        ("onboarding", session_id)
        ) as cursor:
            prompts = (await cursor.fetchone())[0]
            prompts_json = json.loads(prompts)

        return TodayPromptsResponse(
        prompts=prompts_json,
        active_threads=[],
        )   

    

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

   # Get prompts
    async with db.execute(
    """
    SELECT prompts_json FROM prompts
    WHERE source = ? AND session_id = ?
    """, 
    ("generated", session_id)
    ) as cursor:
        prompts = (await cursor.fetchone())[0]
        prompts_json = json.loads(prompts)
    
    
    return TodayPromptsResponse(
        prompts=prompts_json,
        active_threads=active_threads,
    )

