from pydantic import BaseModel
from typing import List
from app.schemas.prompts import Prompt
from app.schemas.threads import Thread
from app.schemas.trees import Tree

class OnboardingRequest(BaseModel):
    session_id: str
    brain_dump: str

class OnboardingResponse(BaseModel):
    starter_prompts: List[Prompt]
    active_threads: List[Thread]
    initial_tree: Tree

class ThreadsAndStarterPrompts(BaseModel):
    starter_prompts: List[Prompt]
    active_threads: List[Thread]

