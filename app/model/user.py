import json
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    name: str
    password: str
    usertype: str
    orgid: int
    deptid: int

class UserLogin(BaseModel):
    email: str
    password: str

class User(json.JSONEncoder):
    def __init__(self, id, email, name, password, usertype, orgid, deptid):
        self.id = id
        self.email = email
        self.name = name
        self.password = password
        self.usertype = usertype
        self.orgid = orgid
        self.deptid = deptid

    # init but all fields are optional
    def __init__(self, id=None, email=None, name=None, password=None, usertype=None, orgid=None, deptid=None):
        self.id = id
        self.email = email
        self.name = name
        self.password = password
        self.usertype = usertype
        self.orgid = orgid
        self.deptid = deptid

    def toJSON(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "usertype": self.usertype
        }
    
