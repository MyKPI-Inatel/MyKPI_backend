from typing import Optional
from pydantic import BaseModel

class QuestionBase(BaseModel):
    id: int
    title: str
    scorefactor: int

class QuestionCreate(BaseModel):
    title: str
    scorefactor: int

class QuestionUpdate(BaseModel):
    title: Optional[str] = None
    scorefactor: Optional[int] = None