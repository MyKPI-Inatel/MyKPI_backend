from typing import List, Optional
from pydantic import BaseModel
from model.question import QuestionBase

class SurveyBase(BaseModel):
    id: int
    title: str
    orgid: int
    questions: Optional[List[QuestionBase]] = None

class SurveyCreate(BaseModel):
    title: str
    orgid: int

class SurveyUpdate(BaseModel):
    title: Optional[str] = None
    orgid: Optional[int] = None

class SurveyResponse(BaseModel):
    id: int
    title: str
    orgid: int