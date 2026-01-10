from pydantic import BaseModel
from typing import List
from app.schemas.trees import Tree

class GardenResponse(BaseModel):
    streak_days: int
    trees: List[Tree]

