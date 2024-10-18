from pydantic import BaseModel
from typing import Optional

class DepartmentBase(BaseModel):
    id: int
    name: str
    orgid: int

class DepartmentCreate(DepartmentBase):
    name: str
    orgid: int

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None