from pydantic import BaseModel, Field
from typing import Literal, Optional

class UserBase(BaseModel):
    id: Optional[int] = None
    email: str
    name: str
    password: str
    usertype: Literal['employee', 'orgadmin', 'superadmin'] = Field(
        ..., 
        description="User type can be one of the following: 'employee', 'orgadmin', 'superadmin'"
    )
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

class UserUpdate(BaseModel):
    name: Optional[str]
    password: Optional[str]
    email: Optional[str]
    usertype: Optional[Literal['employee', 'orgadmin', 'superadmin']] = Field(
        ..., 
        description="User type can be one of the following: 'employee', 'orgadmin', 'superadmin'"
    )
    orgid: Optional[int]
    deptid: Optional[int]
