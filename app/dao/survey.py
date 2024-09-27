from fastapi import HTTPException
from model.survey import SurveyCreate, SurveyUpdate, SurveyBase
import asyncpg
import os

class SurveyDAO:
    @staticmethod
    async def insert(survey: SurveyCreate):
        conn = await get_database()
        try:
            query = """
                INSERT INTO survey (title, orgId)
                VALUES ($1, $2)
                RETURNING id, title, orgId
            """
            async with conn.transaction():
                record = await conn.fetchrow(query, survey.title, survey.org_id)
                return SurveyBase(**record)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to insert survey: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def get_all():
        conn = await get_database()
        try:
            query = """
                SELECT id, title, orgId FROM survey
            """
            records = await conn.fetch(query)
            return [SurveyBase(**record) for record in records]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get surveys: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def get(survey_id: int):
        conn = await get_database()
        try:
            query = """
                SELECT id, title, orgId FROM survey WHERE id = $1
            """
            record = await conn.fetchrow(query, survey_id)
            if record:
                return SurveyBase(**record)
            else:
                raise HTTPException(status_code=404, detail="Survey not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get survey: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def update(survey_id: int, survey: SurveyUpdate):
        conn = await get_database()
        try:
            update_data = survey.dict(exclude_unset=True)
            set_clause = ", ".join([f"{key} = ${i+2}" for i, key in enumerate(update_data.keys())])
            query = f"""
                UPDATE survey SET {set_clause} WHERE id = $1
                RETURNING id, title, orgId
            """

            values = [survey_id] + list(update_data.values())
            async with conn.transaction():
                record = await conn.fetchrow(query, *values)
                if record:
                    return SurveyBase(**record)
                else:
                    raise HTTPException(status_code=404, detail="Survey not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update survey: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def delete(survey_id: int):
        conn = await get_database()
        try:
            query = """
                DELETE FROM survey WHERE id = $1
                RETURNING id
            """
            async with conn.transaction():
                record = await conn.fetchrow(query, survey_id)
                if record:
                    return True
                else:
                    raise HTTPException(status_code=404, detail="Survey not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete survey: {str(e)}")
        finally:
            await conn.close()

# Função para conectar ao banco de dados
async def get_database():
    DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/mykpi") 
    return await asyncpg.connect(DATABASE_URL)
