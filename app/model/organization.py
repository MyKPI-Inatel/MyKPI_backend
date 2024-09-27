from pydantic import BaseModel
from typing import Optional

# Base model for organization
class OrganizationBase(BaseModel):
    id: Optional[int] = None
    name: str

# Model for creating an organization
class OrganizationCreate(OrganizationBase):
    pass

# Model for updating an organization (all fields optional)
class OrganizationUpdate(BaseModel):
    name: Optional[str] = None

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
