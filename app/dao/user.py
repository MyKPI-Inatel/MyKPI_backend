from fastapi import HTTPException
from dao.database import get_database
from model.user import UserBase, UserUpdate

class UserDAO:
    @staticmethod
    async def insert(user: UserBase):
        conn = await get_database()

        try:
            query = """
                INSERT INTO "user" (email, name, password, usertype, orgid, deptid)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING *
            """
            async with conn.transaction():
                result = await conn.fetchrow(query, user.email, user.name, user.password, user.usertype, user.orgid, user.deptid)
                return UserBase(**result)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to insert user: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def exists(email: str):
        conn = await get_database()
        try:
            query = """
                SELECT 1 FROM "user" WHERE email = $1
            """
            result = await conn.fetchval(query, email)
            return result is not None
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to check if user exists: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def get(id: int):
        conn = await get_database()
        try:
            query = """
                SELECT * FROM "user" WHERE id = $1
            """
            result = await conn.fetchrow(query, id)

            user = UserBase(**result)
            return user
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get userss: {str(e)}")
        finally:
            await conn.close()


    @staticmethod
    async def get_by_email(email: str):
        conn = await get_database()
        try:
            query = """
                SELECT * FROM "user" WHERE email = $1
            """
            async with conn.transaction():
                result = await conn.fetchrow(query, email)
                
                user = UserBase(**result) if result else None
                return user
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def delete(id: int):
        conn = await get_database()
        try:
            query = """
                DELETE FROM "user" WHERE id = $1
            """
            result = await conn.execute(query, id)
            return result
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def get_password(email: str):
        conn = await get_database()
        try:
            query = """
                SELECT password FROM "user" WHERE email = $1
            """
            result = await conn.fetchval(query, email)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get password: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def self_update(user: UserUpdate):
        conn = await get_database()
        try:
            query = """
                UPDATE "user"
                SET name = $1, email = $2, password = $3
                WHERE id = $5
            """
            result = await conn.execute(query, user.name, user.email, user.password)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def update(user: UserUpdate):
        conn = await get_database()
        try:
            query = """
                UPDATE "user"
                SET name = $1, password = $2, email = $3, usertype = $4, orgid = $5, deptid = $6
                WHERE id = $7
            """
            result = await conn.execute(query, user.name, user.password, user.email, user.usertype, user.orgid, user.deptid, user.id)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def update_department(user: UserUpdate):
        conn = await get_database()
        try:
            query = """
                UPDATE "user"
                SET name = $1, email = $2, password = $3, usertype = $4, orgid = $5, deptid = $6
                WHERE id = $7
            """
            result = await conn.execute(query, user.name, user.email, user.password, user.usertype, user.orgid, user.deptid, user.id)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")
        finally:
            await conn.close()
