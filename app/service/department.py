
from typing import List

from dao.department import DepartmentDAO

from model.department import DepartmentCreate, DepartmentUpdate, DepartmentBase

class Department:
    @staticmethod
    async def create_department(department_data: DepartmentCreate) -> DepartmentBase:
        return await DepartmentDAO.insert(department_data)

    @staticmethod
    async def get_department(departmentid: int, orgid: int=None) -> DepartmentBase:
        return await DepartmentDAO.get(departmentid, orgid)
    
    @staticmethod
    async def get_department_by_org(orgid: int) -> List[DepartmentBase]:
        return await DepartmentDAO.get_by_org(orgid)

    @staticmethod
    async def update_department(departmentid: int, department_data: DepartmentUpdate, orgid: int=None) -> DepartmentBase:
        return await DepartmentDAO.update(departmentid, department_data, orgid)

    @staticmethod
    async def delete_department(orgid: int, departmentid: int) -> bool:
        return await DepartmentDAO.delete(orgid, departmentid)
    
    @staticmethod
    async def get_last_id() -> int:
        return await DepartmentDAO.get_last_id()
