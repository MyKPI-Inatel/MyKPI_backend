from fastapi import HTTPException
from dao.database import get_database
from model.question import QuestionBase
from model.survey import SurveyCreate, SurveyUpdate, SurveyBase, SurveyResponse
import asyncpg

class SurveyDAO:
    @staticmethod
    async def insert(survey: SurveyCreate):
        conn = await get_database()
        try:
            query = """
                INSERT INTO survey (title, orgid)
                VALUES ($1, $2)
                RETURNING id, title, orgid
            """
            async with conn.transaction():
                record = await conn.fetchrow(query, survey.title, survey.orgid)
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
                SELECT id, title, orgid FROM survey
            """
            records = await conn.fetch(query)
            return [SurveyBase(**record) for record in records]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get surveys: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def get(surveyid: int):
        conn = await get_database()
        try:
            query = """
                SELECT id, title, orgid FROM survey WHERE id = $1
            """
            record = await conn.fetchrow(query, surveyid)
            if record:
                return SurveyBase(**record)
            else:
                raise HTTPException(status_code=404, detail="Survey not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get survey: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def get_by_org(orgid: int):
        conn = await get_database()
        try:
            query = """
                SELECT id, title, orgid FROM survey WHERE orgid = $1
            """
            record = await conn.fetchrow(query, orgid)
            if record:
                return SurveyBase(**record)
            else:
                raise HTTPException(status_code=404, detail="Survey not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get survey: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def update(surveyid: int, survey: SurveyUpdate):
        conn = await get_database()
        try:
            update_data = survey.dict(exclude_unset=True)
            set_clause = ", ".join([f"{key} = ${i+2}" for i, key in enumerate(update_data.keys())])
            query = f"""
                UPDATE survey SET {set_clause} WHERE id = $1
                RETURNING id, title, orgid
            """

            values = [surveyid] + list(update_data.values())
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
    async def delete(surveyid: int):
        conn = await get_database()
        try:
            query = """
                DELETE FROM survey WHERE id = $1
                RETURNING id
            """
            async with conn.transaction():
                record = await conn.fetchrow(query, surveyid)
                if record:
                    return True
                else:
                    raise HTTPException(status_code=404, detail="Survey not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete survey: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def get_questions(surveyid: int):
        conn = await get_database()
        try:
            query = """
                SELECT q.id, q.title, q.scorefactor
                FROM question q
                JOIN surveyquestions sq ON sq.questionid = q.id
                WHERE sq.surveyid = $1
            """
            records = await conn.fetch(query, surveyid)
            if records:
                return [QuestionBase(**record) for record in records]
            else:
                raise HTTPException(status_code=404, detail="No questions found for this survey")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get questions for survey: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def get_unresponded_surveys(employee_id: int):
        conn = await get_database()
        try:
            query = """
                SELECT s.*
                FROM survey s
                WHERE s.id IN (
                    SELECT sq.surveyid
                    FROM surveyquestions sq
                    LEFT JOIN questionscore qs ON sq.questionid = qs.questionid AND qs.employeeid = $1
                    WHERE qs.questionid IS NULL
                )
                AND s.orgid = (
                    SELECT u.orgid
                    FROM "user" u
                    WHERE u.id = $1
                )
            """
            records = await conn.fetch(query, employee_id)
            if records:
                return [SurveyResponse(**record) for record in records]
            else:
                raise HTTPException(status_code=404, detail="No unresponded surveys found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get unresponded surveys: {str(e)}")
        finally:
            await conn.close()