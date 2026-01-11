import aiosqlite
import os
from pathlib import Path

DB_PATH = Path("journal_forest.db")

# SQLite schema from requirements
SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS journal_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    prompt_used TEXT,
    raw_text TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

CREATE TABLE IF NOT EXISTS entry_analysis (
    entry_id INTEGER PRIMARY KEY,
    memory_summary TEXT NOT NULL,
    patterns_reflection TEXT NOT NULL,
    follow_up_question TEXT NOT NULL,
    themes_json TEXT NOT NULL,
    emotions_json TEXT NOT NULL,
    unresolved_json TEXT NOT NULL,
    FOREIGN KEY (entry_id) REFERENCES journal_entries(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS threads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    thread TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    last_seen_entry_id INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

CREATE TABLE IF NOT EXISTS trees (
    entry_id INTEGER PRIMARY KEY,
    session_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    type TEXT NOT NULL,
    rarity TEXT NOT NULL,
    display_name TEXT NOT NULL,
    FOREIGN KEY (entry_id) REFERENCES journal_entries(id) ON DELETE CASCADE,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

CREATE TABLE IF NOT EXISTS streak_days (
    session_id TEXT NOT NULL,
    day TEXT NOT NULL,
    PRIMARY KEY (session_id, day),
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS prompts (
    session_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    source TEXT NOT NULL,
    prompts_json TEXT NOT NULL,
    PRIMARY KEY (session_id, source),
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);
"""

async def get_db():
    """Get database connection"""
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    try:
        yield db
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise
    finally:
        await db.close()

async def init_db():
    """Initialize database with schema"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(SCHEMA)
        await db.commit()
        print(f"Database initialized at {DB_PATH.absolute()}")

async def reset_db():
    """Reset database by deleting and recreating"""
    if DB_PATH.exists():
        DB_PATH.unlink()
    await init_db()

