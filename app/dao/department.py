import asyncpg
from http import HTTPStatus
from fastapi import HTTPException

from dao.database import get_database
from model.department import DepartmentCreate, DepartmentUpdate, DepartmentBase

class DepartmentDAO:
    @staticmethod
    async def insert(department: DepartmentCreate):
        
        conn = await get_database()
        try:
            query = """
                INSERT INTO department (name, orgid)
                VALUES ($1, $2)
                RETURNING id, name, orgid
            """
            async with conn.transaction():
                record = await conn.fetchrow(query, department.name, department.orgid)
                return DepartmentBase(**record)
        except Exception as e:
            raise HTTPException(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                f"Failed to insert department: {str(e)}",
            ) from e
        finally:
            await conn.close()

    @staticmethod
    async def get(deptid: int, orgid: int=None):
        conn = await get_database()
        try:
            query = """
                SELECT id, name, orgid FROM department WHERE id = $1 AND orgid = $2
            """
            record = await conn.fetchrow(query, deptid, orgid)
            if record:
                return DepartmentBase(**record)
            else:
                raise HTTPException(HTTPStatus.NOT_FOUND, "Department not found")
        except asyncpg.PostgresError as e:
            raise HTTPException(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                f"Failed to get department: {str(e)}",
            ) from e
        finally:
            await conn.close()
    
    # get by orgid
    @staticmethod
    async def get_by_org(orgid: int):
        conn = await get_database()
        try:
            query = """
                SELECT id, name, orgid FROM department WHERE orgid = $1
            """
            records = await conn.fetch(query, orgid)
            return [DepartmentBase(**record) for record in records]
        except Exception as e:
            raise HTTPException(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                f"Failed to get departments: {str(e)}",
            ) from e
        finally:
            await conn.close()

    @staticmethod
    async def update(deptid: int, department: DepartmentUpdate, orgid: int=None):
        conn = await get_database()
        try:
            query = """
                UPDATE department SET name = $1 WHERE id = $2 AND orgid = $3
                RETURNING id, name, orgid
            """
            async with conn.transaction():
                record = await conn.fetchrow(query, department.name, deptid, orgid)
                if record:
                    return DepartmentBase(**record)
                else:
                    raise HTTPException(HTTPStatus.NOT_FOUND, "Department not found")
        except Exception as e:
            raise HTTPException(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                f"Failed to update department: {str(e)}",
            ) from e
        finally:
            await conn.close()

    @staticmethod
    async def delete(orgid: int, deptid: int):
        conn = await get_database()
        try:
            query = """
                DELETE FROM department WHERE id = $1 AND orgid = $2
                RETURNING id
            """
            async with conn.transaction():
                record = await conn.fetchrow(query, deptid, orgid)
                if record:
                    return True
                else:
                    raise HTTPException(HTTPStatus.NOT_FOUND, "Department not found")
        except asyncpg.ForeignKeyViolationError as e:
            raise HTTPException(
                HTTPStatus.CONFLICT,
                "Unable to delete department: related data exists in another table.",
            ) from e
        except asyncpg.PostgresError as e:
            raise HTTPException(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                f"Failed to delete department: {str(e)}",
            ) from e
        finally:
            await conn.close()

    @staticmethod
    async def get_last_id():
        conn = await get_database()
        try:
            query = """
                SELECT id FROM department ORDER BY id DESC LIMIT 1
            """
            record = await conn.fetchval(query)
            if record:
                return record
            else:
                raise HTTPException(HTTPStatus.NOT_FOUND, "Department not found")
        except asyncpg.PostgresError as e:
            raise HTTPException(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                f"Failed to get last department: {str(e)}",
            ) from e
        finally:
            await conn.close()