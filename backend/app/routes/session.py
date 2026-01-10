from fastapi import APIRouter, Depends
import uuid
from datetime import datetime
from app.schemas.session import SessionResponse
from app.db.database import get_db
import aiosqlite

router = APIRouter()

@router.post("/session", response_model=SessionResponse)
async def create_session(db: aiosqlite.Connection = Depends(get_db)):
    """Create a new session and return session_id"""
    session_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    
    await db.execute(
        "INSERT INTO sessions (id, created_at, updated_at) VALUES (?, ?, ?)",
        (session_id, now, now)
    )
    await db.commit()
    
    return SessionResponse(session_id=session_id)

