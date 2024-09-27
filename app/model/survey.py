import json
from pydantic import BaseModel

class SurveyBase(BaseModel):
    id: int
    service: str
    org_id: int

class SurveyCreate(BaseModel):
    service: str
    org_id: int

class SurveyUpdate(BaseModel):
    service: str = None
    org_id: int = None

class Survey(json.JSONEncoder):
    def __init__(self, id, title, orgId):
        self.id = id
        self.title = title
        self.orgId = orgId

    # init but all fields are optional
    def __init__(self, id=None, title=None, orgId=None):
        self.id = id
        self.title = title
        self.orgId = orgId

    def toJSON(self):
        return {
            "id": self.id,
            "title": self.title,
            "orgId": self.orgId
        }
    
