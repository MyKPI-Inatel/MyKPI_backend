
from typing import List

from dao.department import DepartmentDAO

from model.department import DepartmentCreate, DepartmentUpdate, DepartmentBase

class Department:
    @staticmethod
    async def create_department(department_data: DepartmentCreate) -> DepartmentBase:
        new_department_data = await DepartmentDAO.insert(department_data)
        return new_department_data

    @staticmethod
    async def get_department(departmentid: int, orgid: int=None) -> DepartmentBase:
        department_data = await DepartmentDAO.get(departmentid, orgid)
        return department_data
    
    @staticmethod
    async def get_department_by_org(orgid: int) -> List[DepartmentBase]:
        department_data = await DepartmentDAO.get_by_org(orgid)
        return department_data

    @staticmethod
    async def update_department(departmentid: int, department_data: DepartmentUpdate, orgid: int=None) -> DepartmentBase:
        updated_department_data = await DepartmentDAO.update(departmentid, department_data, orgid)
        return updated_department_data

    @staticmethod
    async def delete_department(orgid: int, departmentid: int) -> bool:
        return await DepartmentDAO.delete(orgid, departmentid)
    
    @staticmethod
    async def get_last_id() -> int:
        return await DepartmentDAO.get_last_id()
