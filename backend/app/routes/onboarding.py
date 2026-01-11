from typing import Any
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.onboarding import OnboardingRequest, OnboardingResponse
from app.services.llm_service import analyze_brain_dump
from app.services.tree_service import generate_tree
from app.db.database import get_db
import json
from datetime import datetime

router = APIRouter()

@router.post("/onboarding", response_model=OnboardingResponse)
async def submit_onboarding(
    request: OnboardingRequest,
    db: Any = Depends(get_db)
):
    """Process onboarding brain dump and return starter prompts"""
    
    # Verify session exists
    async with db.execute(
        "SELECT id FROM sessions WHERE id = ?", (request.session_id,)
    ) as cursor:
        session = await cursor.fetchone()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
    
    # Analyze brain dump (mock for now)
    analysis = analyze_brain_dump(request.brain_dump)
    
    # Create initial tree (stored in database)
    tree_data = analysis["initial_tree"]
    now = datetime.now().isoformat()
    
    # Note: initial_tree has entry_id=0, store it separately or handle specially
    # For now, we'll create it when first entry is created
    
    # Convert prompts to response format
    starter_prompts = [
        {
            "id": p.id,
            "text": p.text,
            "category": p.category,
        }
        for p in analysis["starter_prompts"]
    ]
    
    # Convert threads to response format (empty for now)
    active_threads = []  # Could extract from brain_dump analysis
    
    return OnboardingResponse(
        starter_prompts=starter_prompts,
        active_threads=active_threads,
        initial_tree={
            "entry_id": 0,
            "session_id": request.session_id,
            "created_at": now,
            "type": tree_data["type"],
            "rarity": tree_data["rarity"],
            "display_name": tree_data["display_name"],
        },
    )

