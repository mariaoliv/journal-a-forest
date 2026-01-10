from fastapi import APIRouter, HTTPException, Depends, Query
from app.schemas.garden import GardenResponse
from app.db.database import get_db
import aiosqlite

router = APIRouter()

@router.get("/garden", response_model=GardenResponse)
async def get_garden(
    session_id: str = Query(..., description="Session ID"),
    db: aiosqlite.Connection = Depends(get_db)
):
    """Get streak and all trees for a session"""
    
    # Verify session exists
    async with db.execute(
        "SELECT id FROM sessions WHERE id = ?", (session_id,)
    ) as cursor:
        session = await cursor.fetchone()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
    
    # Get streak
    async with db.execute(
        "SELECT COUNT(DISTINCT day) FROM streak_days WHERE session_id = ?",
        (session_id,)
    ) as cursor:
        streak_row = await cursor.fetchone()
        streak_days = streak_row[0] if streak_row else 0
    
    # Get all trees
    async with db.execute(
        """
        SELECT entry_id, session_id, created_at, type, rarity, display_name
        FROM trees
        WHERE session_id = ?
        ORDER BY created_at DESC
        """,
        (session_id,)
    ) as cursor:
        tree_rows = await cursor.fetchall()
    
    trees = [
        {
            "entry_id": row[0],
            "session_id": row[1],
            "created_at": row[2],
            "type": row[3],
            "rarity": row[4],
            "display_name": row[5],
        }
        for row in tree_rows
    ]
    
    return GardenResponse(
        streak_days=streak_days,
        trees=trees,
    )

