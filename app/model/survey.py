from pydantic import BaseModel
from typing import List, Optional

from model.question import QuestionBase

class SurveyBase(BaseModel):
    id: int
    title: str
    orgid: int

class SurveyCreate(BaseModel):
    title: str
    orgid: int

class SurveyUpdate(BaseModel):
    title: Optional[str] = None

class SurveyResponse(BaseModel):
    id: int
    title: str
    orgid: int