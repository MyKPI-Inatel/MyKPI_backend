from fastapi import HTTPException
from model.department import DepartmentCreate, DepartmentUpdate, DepartmentBase
import asyncpg
import os

class DepartmentDAO:
    @staticmethod
    async def insert(department: DepartmentCreate):
        conn = await get_database()
        try:
            query = """
                INSERT INTO department (name, orgid)
                VALUES ($1, $2)
                RETURNING id, name
            """
            async with conn.transaction():
                record = await conn.fetchrow(query, department.name, department.orgid)
                return DepartmentBase(**record)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to insert department: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def get_all():
        conn = await get_database()
        try:
            query = """
                SELECT id, name, orgid FROM department
            """
            records = await conn.fetch(query)
            return [DepartmentBase(**record) for record in records]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get departments: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def get(orgid: int):
        conn = await get_database()
        try:
            query = """
                SELECT id, name, orgid FROM department WHERE id = $1
            """
            record = await conn.fetchrow(query, orgid)
            if record:
                return DepartmentBase(**record)
            else:
                raise HTTPException(status_code=404, detail="Department not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get department: {str(e)}")
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
            raise HTTPException(status_code=500, detail=f"Failed to get departments: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def update(orgid: int, department: DepartmentUpdate):
        conn = await get_database()
        try:
            update_data = department.dict(exclude_unset=True)
            set_clause = ", ".join([f"{key} = ${i+2}" for i, key in enumerate(update_data.keys())])
            query = f"""
                UPDATE department SET {set_clause} WHERE id = $1
                RETURNING id, name
            """

            values = [orgid] + list(update_data.values())
            async with conn.transaction():
                record = await conn.fetchrow(query, *values)
                if record:
                    return DepartmentBase(**record)
                else:
                    raise HTTPException(status_code=404, detail="Department not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update department: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def delete(orgid: int):
        conn = await get_database()
        try:
            query = """
                DELETE FROM department WHERE id = $1
                RETURNING id
            """
            async with conn.transaction():
                record = await conn.fetchrow(query, orgid)
                if record:
                    return True
                else:
                    raise HTTPException(status_code=404, detail="Department not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete department: {str(e)}")
        finally:
            await conn.close()

# Função para conectar ao banco de dados
async def get_database():
    DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/mykpi") 
    return await asyncpg.connect(DATABASE_URL)
