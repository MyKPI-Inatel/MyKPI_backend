from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from internal.security import get_current_user, verify_permissions
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
    verify_permissions(current_user, UserType.superadmin)
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
    verify_permissions(current_user, UserType.superadmin)
    return await Organization.get_all_organizations()

@router.get(
    "/{orgid}",
    status_code=HTTPStatus.OK,
    response_model=OrganizationBase, 
    summary="Get a organization by ID", 
    description="Retrieve a specific organization by its ID."
)
async def get_organization(orgid: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    verify_permissions(current_user, UserType.orgadmin, {'orgid': orgid})
    organization = await Organization.get_organization(orgid)
    if organization is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Organization not found")
    return organization

@router.put(
    "/{orgid}",
    status_code=HTTPStatus.OK,
    response_model=OrganizationBase, 
    summary="Update a organization", 
    description="Update the details of a specific organization by its ID."
)
async def update_organization(orgid: int, organization: OrganizationUpdate,
    current_user: CurrentUser = Depends(get_current_user)
):
    verify_permissions(current_user, UserType.orgadmin, {'orgid': orgid})
    updated_organization = await Organization.update_organization(orgid, organization)
    if updated_organization is None:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Error updating organization")
    return updated_organization

@router.delete(
    "/{orgid}",
    status_code=HTTPStatus.OK,
    summary="Delete a organization", 
    description="Delete a specific organization by its ID."
)
async def delete_organization(orgid: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    verify_permissions(current_user, UserType.superadmin)
    result = await Organization.delete_organization(orgid)
    if not result:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Organization not found")
    return {"message": "Organization deleted successfully"}
