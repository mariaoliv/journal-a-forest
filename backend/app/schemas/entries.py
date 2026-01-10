from pydantic import BaseModel
from typing import List, Optional
from app.schemas.prompts import Prompt
from app.schemas.trees import Tree

class EntryRequest(BaseModel):
    session_id: str
    prompt_id: Optional[str] = None
    text: str

class EntryResponse(BaseModel):
    entry_id: int
    memory_summary: str
    patterns_reflection: str
    follow_up_question: str
    themes: List[str]
    emotions: List[str]
    new_prompts: List[Prompt]
    tree: Tree
    streak_updated: int

