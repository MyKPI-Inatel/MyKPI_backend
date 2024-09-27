import json
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    name: str
    password: str
    usertype: str
    orgid: int
    deptId: int

class UserLogin(BaseModel):
    email: str
    password: str

class User(json.JSONEncoder):
    def __init__(self, id, email, name, password, usertype, orgid, deptId):
        self.id = id
        self.email = email
        self.name = name
        self.password = password
        self.usertype = usertype
        self.orgid = orgid
        self.deptId = deptId

    # init but all fields are optional
    def __init__(self, email=None, name=None, password=None, usertype=None, orgid=None, deptId=None):
        self.email = email
        self.name = name
        self.password = password
        self.usertype = usertype
        self.orgid = orgid
        self.deptId = deptId

    def toJSON(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "usertype": self.usertype
        }
    
