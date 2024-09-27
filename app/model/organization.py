from pydantic import BaseModel
from typing import Optional

# Base model for organization
class OrganizationBase(BaseModel):
    id: int
    name: str

# Model for creating an organization
class OrganizationCreate(OrganizationBase):
    name: str

# Model for updating an organization (all fields optional)
class OrganizationUpdate(BaseModel):
    name: str = None

# Organization class to represent the table and handle JSON serialization
class Organization:
    def __init__(self, id: Optional[int] = None, name: Optional[str] = None):
        self.id = id
        self.name = name

    def toJSON(self):
        return {
            "id": self.id,
            "name": self.name
        }
