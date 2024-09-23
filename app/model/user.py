import json
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    name: str
    password: str
    usertype: str
    orgId: int
    deptId: int

class UserLogin(BaseModel):
    email: str
    password: str

class User(json.JSONEncoder):
    def __init__(self, id, email, name, password, usertype, orgId, deptId):
        self.id = id
        self.email = email
        self.name = name
        self.password = password
        self.usertype = usertype
        self.orgId = orgId
        self.deptId = deptId

    # init but all fields are optional
    def __init__(self, email=None, name=None, password=None, usertype=None, orgId=None, deptId=None):
        self.email = email
        self.name = name
        self.password = password
        self.usertype = usertype
        self.orgId = orgId
        self.deptId = deptId

    def toJSON(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "usertype": self.usertype
        }
    
