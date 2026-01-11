from fastapi import APIRouter, HTTPException, Depends
from app.schemas.entries import EntryRequest, EntryResponse
from app.services.llm_service import analyze_entry, generate_prompts
from app.services.chroma_service import ChromaService
from app.services.tree_service import generate_tree
from app.services.chroma_service import chroma_service
from app.db.database import get_db
import aiosqlite
import json
from datetime import datetime, date

router = APIRouter()
chroma_db = ChromaService()

@router.post("/entries", response_model=EntryResponse)
async def create_entry(
    request: EntryRequest,
    db: aiosqlite.Connection = Depends(get_db)
):
    """Create a journal entry and return analysis, prompts, and tree"""
    
    # Verify session exists
    async with db.execute(
        "SELECT id FROM sessions WHERE id = ?", (request.session_id,)
    ) as cursor:
        session = await cursor.fetchone()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
    
    now = datetime.now().isoformat()
    
    # Insert journal entry
    result = await db.execute(
        """
        INSERT INTO journal_entries (session_id, created_at, prompt_used, raw_text)
        VALUES (?, ?, ?, ?)
        """,
        (request.session_id, now, request.prompt_id, request.text)
    )
    await db.commit()
    
    entry_id = result.lastrowid
    
    if not entry_id:
        raise HTTPException(status_code=500, detail="Failed to create entry")
    
    # Analyze entry (mock for now)
    analysis = analyze_entry(request.text, request.prompt_id)
    
    # Store analysis
    await db.execute(
        """
        INSERT INTO entry_analysis (
            entry_id, memory_summary, patterns_reflection, follow_up_question,
            themes_json, emotions_json, unresolved_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            entry_id,
            analysis["memory_summary"],
            analysis["patterns_reflection"],
            analysis["follow_up_question"],
            json.dumps(analysis["themes"]),
            json.dumps(analysis["emotions"]),
            json.dumps(analysis["unresolved"]),
        )
    )
    
    # Generate tree
    tree_data = generate_tree(
        request.text,
        entry_id,
        analysis["themes"],
        analysis["emotions"]
    )
    
    # Store tree
    await db.execute(
        """
        INSERT INTO trees (entry_id, session_id, created_at, type, rarity, display_name)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            entry_id,
            request.session_id,
            now,
            tree_data["type"],
            tree_data["rarity"],
            tree_data["display_name"],
        )
    )
    
    # Update streak
    today = date.today().isoformat()
    await db.execute(
        """
        INSERT OR IGNORE INTO streak_days (session_id, day)
        VALUES (?, ?)
        """,
        (request.session_id, today)
    )
    
    # Get current streak
    async with db.execute(
        "SELECT COUNT(DISTINCT day) FROM streak_days WHERE session_id = ?",
        (request.session_id,)
    ) as cursor:
        streak_row = await cursor.fetchone()
        streak_updated = streak_row[0] if streak_row else 0
    
    # Update session updated_at
    await db.execute(
        "UPDATE sessions SET updated_at = ? WHERE id = ?",
        (now, request.session_id)
    )
    
    await db.commit()
    
    # Store in Chroma 
    chroma_service.store_entry(
        entry_id,
        request.session_id,
        analysis["memory_summary"],
        metadata={
            "themes": analysis["themes"],
            "emotions": analysis["emotions"],
            "unresolved": analysis["unresolved"],
            "follow_up_question": analysis["follow_up_question"],
            "patterns_reflection": analysis["patterns_reflection"],
            "created_at": now,
            "entry_id": entry_id
        }
    )
    
    # Get session history (for prompt generation)
    async with db.execute(
        """
        SELECT memory_summary, entry_id
        FROM entry_analysis ea
        JOIN journal_entries je ON ea.entry_id = je.id
        WHERE session_id = ?
        ORDER BY created_at DESC
        LIMIT 3
        """,
        (request.session_id,)
    ) as cursor:
        recent_entries = await cursor.fetchall()

    async with db.execute(
        """
        SELECT id, thread, status, created_at, updated_at, last_seen_entry_id
        FROM threads
        WHERE session_id = ? AND status = 'active'
        ORDER BY updated_at DESC
        LIMIT 3
        """,
        (request.session_id,)
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

    similarity_search_results = chroma_db.search_similar(query=summary, session_id=request.session_id, exclude_entry_ids=recent_entry_ids, limit=5)

    session_history = {
        "recent_memories": recent_summaries,
        "relevant_memories": similarity_search_results,
        "active_threads": active_threads
    }

    # Generate new prompts 

    text = f'{analysis["memory_summary"]}\n{analysis["follow_up_question"]}\nThemes: {analysis["themes"]}\nEmotions: {analysis["emotions"]}'
    new_prompts_data = generate_prompts(text, session_history)
    new_prompts = [
        {
            "id": p["id"],
            "text": p["text"],
            "category": p.get("category"),
        }
        for p in new_prompts_data[:3]  # Return 1-3 prompts
    ]

    async with db.execute(
        """
        SELECT COUNT(*) FROM prompts
        WHERE session_id = ? AND source = ?
        """,
        (request.session_id, "generated")
    ) as cursor:
        num_generated_prompts = (await cursor.fetchone())[0]

    if num_generated_prompts == 0:
        await db.execute(
            """
            INSERT INTO prompts (
                session_id, created_at, source, prompts_json
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                request.session_id,
                now,
                "generated",
                json.dumps(new_prompts)
            )
        )
    else:
         await db.execute(
            """
            UPDATE prompts
            SET prompts_json = ?, created_at = ?
            WHERE session_id = ? AND source = ?
            """,
            (
                json.dumps(new_prompts),
                now,
                request.session_id,
                "generated"
            )
        )

    
    return EntryResponse(
        entry_id=entry_id,
        memory_summary=analysis["memory_summary"],
        patterns_reflection=analysis["patterns_reflection"],
        follow_up_question=analysis["follow_up_question"],
        themes=analysis["themes"],
        emotions=analysis["emotions"],
        new_prompts=new_prompts,
        tree={
            "entry_id": entry_id,
            "session_id": request.session_id,
            "created_at": now,
            "type": tree_data["type"],
            "rarity": tree_data["rarity"],
            "display_name": tree_data["display_name"],
        },
        streak_updated=streak_updated,
    )

