from pydantic import BaseModel
from typing import Optional, Literal

class Thread(BaseModel):
    id: int
    thread: str
    status: Literal["active", "snoozed", "resolved"]
    created_at: str
    updated_at: str
    last_seen_entry_id: Optional[int] = None

class ThreadUpdateRequest(BaseModel):
    status: Literal["active", "snoozed", "resolved"]

