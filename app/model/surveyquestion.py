from typing import Optional
from pydantic import BaseModel

class SurveyQuestionBase(BaseModel):
    surveyid: int
    questionid: int

class SurveyQuestionCreate(BaseModel):
    surveyid: int
    questionid: int

class SurveyQuestionUpdate(BaseModel):
    surveyid: Optional[int] = None
    questionid: Optional[int] = None