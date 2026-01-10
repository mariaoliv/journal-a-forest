from pydantic import BaseModel
from typing import Literal

class Tree(BaseModel):
    entry_id: int
    session_id: str
    created_at: str
    type: str
    rarity: Literal["common", "uncommon", "rare", "epic", "legendary"]
    display_name: str

