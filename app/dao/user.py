from fastapi import HTTPException
from app.dao.database import get_database
from model.user import UserBase
from passlib.context import CryptContext
import asyncpg


# Crie o contexto de segurança para o hash da senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserDAO:
    @staticmethod
    async def insert(user: UserBase):
        conn = await get_database()
        if await UserDAO.exists(user.email, conn):
            raise HTTPException(status_code=400, detail="User already exists")

        # Hash da senha antes de inserir no banco de dados
        hashed_password = pwd_context.hash(user.password)

        try:
            query = """
                INSERT INTO "user" (email, name, password, usertype, orgid, deptid)
                VALUES ($1, $2, $3, $4, $5, $6)
            """
            async with conn.transaction():
                result = await conn.execute(query, user.email, user.name, hashed_password, user.usertype, user.orgid, user.deptid)
                return result
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to insert user: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def exists(email: str, conn):
        try:
            query = """
                SELECT 1 FROM "user" WHERE email = $1
            """
            result = await conn.fetchval(query, email)
            return result is not None
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to check if user exists: {str(e)}")

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
            result = await conn.fetchrow(query, email)

            user = UserBase(**result)
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