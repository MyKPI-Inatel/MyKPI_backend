import json
from pydantic import BaseModel

class QuestionBase(BaseModel):
    id: int
    title: str
    questionid: int

class QuestionCreate(BaseModel):
    title: str
    questionid: int

class QuestionUpdate(BaseModel):
    title: str = None
    questionid: int = None

class Question(json.JSONEncoder):
    def __init__(self, id, title, questionid):
        self.id = id
        self.title = title
        self.questionid = questionid

    # init but all fields are optional
    def __init__(self, id=None, title=None, questionid=None):
        self.id = id
        self.title = title
        self.questionid = questionid

    def toJSON(self):
        return {
            "id": self.id,
            "title": self.title,
            "questionid": self.questionid
        }
    
