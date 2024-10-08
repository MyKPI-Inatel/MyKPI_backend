import json
from pydantic import BaseModel

class SurveyBase(BaseModel):
    id: int
    title: str
    orgid: int

class SurveyCreate(BaseModel):
    title: str
    orgid: int

class SurveyUpdate(BaseModel):
    title: str = None
    orgid: int = None

class Survey(json.JSONEncoder):
    def __init__(self, id, title, orgid):
        self.id = id
        self.title = title
        self.orgid = orgid

    # init but all fields are optional
    def __init__(self, id=None, title=None, orgid=None):
        self.id = id
        self.title = title
        self.orgid = orgid

    def setQuestions(self, questions):
        self.questions = questions

    def toJSON(self):
        return {
            "id": self.id,
            "title": self.title,
            "orgid": self.orgid
        }
    
