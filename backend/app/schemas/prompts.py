from pydantic import BaseModel
from typing import Optional
from typing import List
from uuid import UUID, uuid1

class Prompt(BaseModel):
    id: str
    text: str
    category: Optional[str] = None

    @classmethod
    def create(cls, text: str, category: Optional[str] = None) -> "Prompt":
        return cls(id=uuid1(), text=text, category=category)

class Prompts(BaseModel):
    prompts: List[Prompt]

class TodayPromptsResponse(BaseModel):
    prompts: List[Prompt]
    active_threads: List["Thread"]

from app.schemas.threads import Thread
TodayPromptsResponse.model_rebuild()

