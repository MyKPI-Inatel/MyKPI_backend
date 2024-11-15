from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from internal.security import get_current_user
from model.user import UserType, CurrentUser
from model.organization import OrganizationBase, OrganizationCreate, OrganizationUpdate

from service.organization import Organization

router = APIRouter()

@router.post("/",
    status_code=HTTPStatus.CREATED,
    response_model=OrganizationBase, 
    summary="Create a new organization", 
    description="This endpoint allows you to create a new organization."
)
async def create_organization(organization: OrganizationCreate,
    current_user: CurrentUser = Depends(get_current_user)
):
    return await Organization.create_organization(organization)

@router.get("/",
    status_code=HTTPStatus.OK,
    response_model=List[OrganizationBase], 
    summary="Get all organizations", 
    description="Retrieve a list of all organizations."
)
async def get_organizations(
    current_user: CurrentUser = Depends(get_current_user)
):
    return await Organization.get_all_organizations()

@router.get(
    "/{organizationid}",
    status_code=HTTPStatus.OK,
    response_model=OrganizationBase, 
    summary="Get a organization by ID", 
    description="Retrieve a specific organization by its ID."
)
async def get_organization(organizationid: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    organization = await Organization.get_organization(organizationid)
    if organization is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Organization not found")
    return organization

@router.put(
    "/{organizationid}",
    status_code=HTTPStatus.OK,
    response_model=OrganizationBase, 
    summary="Update a organization", 
    description="Update the details of a specific organization by its ID."
)
async def update_organization(organizationid: int, organization: OrganizationUpdate,
    current_user: CurrentUser = Depends(get_current_user)
):
    updated_organization = await Organization.update_organization(organizationid, organization)
    if updated_organization is None:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Error updating organization")
    return updated_organization

@router.delete(
    "/{organizationid}",
    status_code=HTTPStatus.OK,
    summary="Delete a organization", 
    description="Delete a specific organization by its ID."
)
async def delete_organization(organizationid: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    result = await Organization.delete_organization(organizationid)
    if not result:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Organization not found")
    return {"message": "Organization deleted successfully"}
