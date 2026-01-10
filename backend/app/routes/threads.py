from fastapi import APIRouter, HTTPException, Depends
from app.schemas.threads import ThreadUpdateRequest
from app.db.database import get_db
import aiosqlite
from datetime import datetime

router = APIRouter()

@router.post("/{thread_id}")
async def update_thread(
    thread_id: int,
    request: ThreadUpdateRequest,
    db: aiosqlite.Connection = Depends(get_db)
):
    """Update thread status (activate/snooze/resolve)"""
    
    # Verify thread exists
    async with db.execute(
        "SELECT id, session_id FROM threads WHERE id = ?", (thread_id,)
    ) as cursor:
        thread = await cursor.fetchone()
        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")
    
    # Update thread status
    now = datetime.utcnow().isoformat()
    await db.execute(
        """
        UPDATE threads 
        SET status = ?, updated_at = ?
        WHERE id = ?
        """,
        (request.status, now, thread_id)
    )
    await db.commit()
    
    return {"message": "Thread updated successfully", "thread_id": thread_id}

