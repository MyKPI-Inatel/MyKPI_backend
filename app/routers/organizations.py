from fastapi import APIRouter, HTTPException
from typing import List
from model.organization import OrganizationBase, OrganizationCreate, OrganizationUpdate
from service.organization import Organization as OrganizationService

router = APIRouter()

@router.post(
    "", 
    response_model=OrganizationBase, 
    summary="Create a new organization", 
    description="This endpoint allows you to create a new organization in the system."
)
async def create_organization(organization: OrganizationCreate):
    new_organization = await OrganizationService.create_organization(organization)
    return new_organization

@router.get(
    "", 
    response_model=List[OrganizationBase], 
    summary="Get all organizations", 
    description="Retrieve a list of all organizations in the system."
)
async def get_organizations():
    organizations = await OrganizationService.get_all_organizations()
    return organizations

@router.get(
    "/{organizationid}", 
    response_model=OrganizationBase, 
    summary="Get a organization by ID", 
    description="Retrieve a specific organization by its ID."
)
async def get_organization(organizationid: int):
    organization = await OrganizationService.get_organization(organizationid)
    if organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@router.put(
    "/{organizationid}", 
    response_model=OrganizationBase, 
    summary="Update a organization", 
    description="Update the details of a specific organization by its ID."
)
async def update_organization(organizationid: int, organization: OrganizationUpdate):
    updated_organization = await OrganizationService.update_organization(organizationid, organization)
    if updated_organization is None:
        raise HTTPException(status_code=400, detail="Error updating organization")
    return updated_organization

@router.delete(
    "/{organizationid}", 
    summary="Delete a organization", 
    description="Delete a specific organization by its ID."
)
async def delete_organization(organizationid: int):
    result = await OrganizationService.delete_organization(organizationid)
    if not result:
        raise HTTPException(status_code=404, detail="Organization not found")
    return {"message": "Organization deleted successfully"}
