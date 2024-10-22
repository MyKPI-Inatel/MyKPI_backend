from fastapi import HTTPException
from app.dao.database import get_database
from model.organization import OrganizationCreate, OrganizationUpdate, OrganizationBase

class OrganizationDAO:
    @staticmethod
    async def insert(organization: OrganizationCreate):
        conn = await get_database()
        try:
            query = """
                INSERT INTO organization (name)
                VALUES ($1)
                RETURNING id, name
            """
            async with conn.transaction():
                record = await conn.fetchrow(query, organization.name)
                return OrganizationBase(**record)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to insert organization: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def get_all():
        conn = await get_database()
        try:
            query = """
                SELECT id, name FROM organization
            """
            records = await conn.fetch(query)
            return [OrganizationBase(**record) for record in records]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get organizations: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def get(orgid: int):
        conn = await get_database()
        try:
            query = """
                SELECT id, name FROM organization WHERE id = $1
            """
            record = await conn.fetchrow(query, orgid)
            if record:
                return OrganizationBase(**record)
            else:
                raise HTTPException(status_code=404, detail="Organization not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get organization: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def update(orgid: int, organization: OrganizationUpdate):
        conn = await get_database()
        try:
            update_data = organization.dict(exclude_unset=True)
            set_clause = ", ".join([f"{key} = ${i+2}" for i, key in enumerate(update_data.keys())])
            query = f"""
                UPDATE organization SET {set_clause} WHERE id = $1
                RETURNING id, name
            """

            values = [orgid] + list(update_data.values())
            async with conn.transaction():
                record = await conn.fetchrow(query, *values)
                if record:
                    return OrganizationBase(**record)
                else:
                    raise HTTPException(status_code=404, detail="Organization not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update organization: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def delete(orgid: int):
        conn = await get_database()
        try:
            query = """
                DELETE FROM organization WHERE id = $1
                RETURNING id
            """
            async with conn.transaction():
                record = await conn.fetchrow(query, orgid)
                if record:
                    return True
                else:
                    raise HTTPException(status_code=404, detail="Organization not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete organization: {str(e)}")
        finally:
            await conn.close()