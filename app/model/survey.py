import json
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

class Survey(json.JSONEncoder):
    def __init__(self, id=None, title=None, orgid=None):
        self.id = id
        self.title = title
        self.orgid = orgid
        self.questions = []

    def setQuestions(self, questions: List[QuestionBase]):
        self.questions = questions

    def toJSON(self):
        return {
            "id": self.id,
            "title": self.title,
            "orgid": self.orgid,
            "questions": [q.dict() for q in self.questions] if self.questions else []
        }
