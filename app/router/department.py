from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from internal.security import get_current_user, verify_permissions
from model.user import UserType, CurrentUser
from model.department import DepartmentBase, DepartmentCreate, DepartmentUpdate

from service.department import Department

router = APIRouter()

@router.post(
    "/", 
    response_model=DepartmentBase, 
    summary="Create a new department", 
    description="This endpoint allows you to create a new department."
)
async def create_department(department: DepartmentCreate,
    current_user: CurrentUser = Depends(get_current_user)
):
    verify_permissions(current_user, UserType.orgadmin, {'orgid': department.orgid})
    return await Department.create_department(department)

@router.get(
    "/org/{orgid}", 
    response_model=List[DepartmentBase], 
    summary="Get all departments by organization ID", 
    description="Retrieve a list of all departments associated with a specific organization ID."
)
async def get_departments(orgid: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    verify_permissions(current_user, UserType.orgadmin, {'orgid': orgid})
    return await Department.get_department_by_org(orgid)

@router.get(
    "/org/{orgid}/{departmentid}", 
    response_model=DepartmentBase, 
    summary="Get a department by ID", 
    description="Retrieve a specific department by its ID."
)
async def get_department(departmentid: int, orgid: int=None,
    current_user: CurrentUser = Depends(get_current_user)
):
    verify_permissions(current_user, UserType.orgadmin, {'orgid': orgid})
    department = await Department.get_department(departmentid, orgid)
    if department is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Department not found")
    return department

@router.put(
    "/org/{orgid}/{departmentid}", 
    response_model=DepartmentBase, 
    summary="Update a department", 
    description="Update the details of a specific department by its ID."
)
async def update_department(departmentid: int, department: DepartmentUpdate, orgid: int=None,
    current_user: CurrentUser = Depends(get_current_user)
):
    verify_permissions(current_user, UserType.orgadmin, {'orgid': orgid})
    updated_department = await Department.update_department(departmentid, department, orgid)
    if updated_department is None:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Error updating department")
    return updated_department

@router.delete(
    "/org/{orgid}/{departmentid}", 
    summary="Delete a department", 
    description="Delete a specific department by its ID."
)
async def delete_department(orgid: int, departmentid: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    verify_permissions(current_user, UserType.orgadmin, {'orgid': orgid})
    result = await Department.delete_department(orgid, departmentid)
    if not result:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Department not found")
    return {"message": "Department deleted successfully"}
