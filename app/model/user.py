from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    id: Optional[int] = None
    email: str
    name: str
    password: str
    usertype: str
    orgid: int
    deptid: int

    def toJSON(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "usertype": self.usertype,
            "orgid": self.orgid,
            "deptid": self.deptid
        }

class UserLogin(BaseModel):
    email: str
    password: str
