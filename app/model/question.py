from typing import Optional
from pydantic import BaseModel

class QuestionBase(BaseModel):
    id: int
    title: str
    scorefactor: int
    surveyid: Optional[int] = None

class QuestionCreate(BaseModel):
    title: str
    scorefactor: int
    surveyid: int

class QuestionUpdate(BaseModel):
    title: Optional[str] = None
    scorefactor: Optional[int] = None

class ScoredQuestion(BaseModel):
    questionid: int
    score: int

class QuestionToScore(BaseModel):
    employeeid: int
    surveyid: int
    answers: list[ScoredQuestion]