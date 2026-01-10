from fastapi import APIRouter, HTTPException, Depends, Query
from app.db.database import get_db
from app.services.chroma_service import chroma_service
import aiosqlite

router = APIRouter()

@router.delete("/memories")
async def delete_memories(
    session_id: str = Query(..., description="Session ID"),
    db: aiosqlite.Connection = Depends(get_db)
):
    """Delete all memories, entries, trees, and vectors for a session"""
    
    # Verify session exists
    async with db.execute(
        "SELECT id FROM sessions WHERE id = ?", (session_id,)
    ) as cursor:
        session = await cursor.fetchone()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
    
    # Delete in order (respecting foreign keys)
    # Trees are deleted via CASCADE when entries are deleted
    # Entry analyses are deleted via CASCADE when entries are deleted
    
    # Delete streak days
    await db.execute(
        "DELETE FROM streak_days WHERE session_id = ?",
        (session_id,)
    )
    
    # Get entry IDs before deletion (for Chroma)
    async with db.execute(
        "SELECT id FROM journal_entries WHERE session_id = ?",
        (session_id,)
    ) as cursor:
        entry_ids = [row[0] for row in await cursor.fetchall()]
    
    # Delete entries (CASCADE will handle trees and analyses)
    await db.execute(
        "DELETE FROM journal_entries WHERE session_id = ?",
        (session_id,)
    )
    
    # Delete threads
    await db.execute(
        "DELETE FROM threads WHERE session_id = ?",
        (session_id,)
    )
    
    # Note: We keep the session record for now
    # To fully delete, uncomment:
    # await db.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    
    await db.commit()
    
    # Delete from Chroma (stubbed)
    chroma_service.delete_session_entries(session_id)
    
    return {
        "message": "All memories deleted successfully",
        "session_id": session_id,
        "entries_deleted": len(entry_ids),
    }

