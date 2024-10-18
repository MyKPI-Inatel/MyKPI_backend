from pydantic import BaseModel
from typing import Optional

class OrganizationBase(BaseModel):
    id: int
    name: str

class OrganizationCreate(BaseModel):
    name: str

class OrganizationUpdate(BaseModel):
    name: Optional[str] = None