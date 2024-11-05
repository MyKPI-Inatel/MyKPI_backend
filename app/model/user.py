from pydantic import BaseModel
from typing import Optional

from enum import Enum

class UserType(str, Enum):
    employee = 'employee'
    orgadmin = 'orgadmin'
    superadmin = 'superadmin'
    
    @property
    def level(self) -> int:
        levels = {
            UserType.employee: 1,
            UserType.orgadmin: 2,
            UserType.superadmin: 3
        }
        return levels[self]

class UserBase(BaseModel):
    id: Optional[int] = None
    email: str
    name: str
    password: str
    usertype: UserType
    orgid: int
    deptid: int

class UserLogin(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    email: str
    name: str
    password: str
    orgid: int
    deptid: int

class EmployeeCreate(BaseModel):
    email: str
    name: str
    deptid: int

class UserUpdate(BaseModel):
    name: Optional[str]
    password: Optional[str]
    email: Optional[str]
    usertype: Optional[UserType]
    orgid: Optional[int]
    deptid: Optional[int]