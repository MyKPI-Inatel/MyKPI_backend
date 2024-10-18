from fastapi import APIRouter, HTTPException
from typing import List
from model.department import DepartmentBase, DepartmentCreate, DepartmentUpdate
from service.department import Department as DepartmentService

router = APIRouter()

@router.post(
    "", 
    response_model=DepartmentBase, 
    summary="Create a new department", 
    description="This endpoint allows you to create a new department."
)
async def create_department(department: DepartmentCreate):
    new_department = await DepartmentService.create_department(department)
    return new_department

@router.get(
    "/org/{orgid}", 
    response_model=List[DepartmentBase], 
    summary="Get all departments by organization ID", 
    description="Retrieve a list of all departments associated with a specific organization ID."
)
async def get_departments(orgid: int):
    departments = await DepartmentService.get_department_by_org(orgid)
    return departments

@router.get(
    "/{departmentid}", 
    response_model=DepartmentBase, 
    summary="Get a department by ID", 
    description="Retrieve a specific department by its ID."
)
async def get_department(departmentid: int):
    department = await DepartmentService.get_department(departmentid)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@router.put(
    "/{departmentid}", 
    response_model=DepartmentBase, 
    summary="Update a department", 
    description="Update the details of a specific department by its ID."
)
async def update_department(departmentid: int, department: DepartmentUpdate):
    updated_department = await DepartmentService.update_department(departmentid, department)
    if updated_department is None:
        raise HTTPException(status_code=400, detail="Error updating department")
    return updated_department

@router.delete(
    "/{departmentid}", 
    summary="Delete a department", 
    description="Delete a specific department by its ID."
)
async def delete_department(orgid: int, departmentid: int):
    result = await DepartmentService.delete_department(orgid, departmentid)
    if not result:
        raise HTTPException(status_code=404, detail="Department not found")
    return {"message": "Department deleted successfully"}
