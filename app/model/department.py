from pydantic import BaseModel
from typing import Optional

# Base model for Department
class DepartmentBase(BaseModel):
    id: int
    name: str
    orgid: int

# Model for creating an Department
class DepartmentCreate(DepartmentBase):
    name: str

# Model for updating an Department (all fields optional)
class DepartmentUpdate(BaseModel):
    name: str = None

# Department class to represent the table and handle JSON serialization
class Department:
    def __init__(self, id: Optional[int] = None, name: Optional[str] = None, orgid: Optional[int] = None):
        self.id = id
        self.name = name
        self.orgid = orgid

    def toJSON(self):
        return {
            "id": self.id,
            "name": self.name,
            "orgid": self.orgid
        }
