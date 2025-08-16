from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QuoteCreate(BaseModel):
    text: str
    author: str

class QuoteOut(BaseModel):
    id: int
    text: str
    author: str
    owner_id: Optional[int]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
