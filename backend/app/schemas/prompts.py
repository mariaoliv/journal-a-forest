from pydantic import BaseModel
from typing import Optional
from typing import List

class Prompt(BaseModel):
    id: str
    text: str
    category: Optional[str] = None

class TodayPromptsResponse(BaseModel):
    prompts: List[Prompt]
    active_threads: List["Thread"]

from app.schemas.threads import Thread
TodayPromptsResponse.model_rebuild()

