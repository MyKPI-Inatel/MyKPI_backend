import asyncpg
from http import HTTPStatus
from fastapi import HTTPException

from dao.database import get_database
from model.surveyquestion import SurveyQuestionBase

class SurveyQuestionDAO:
    @staticmethod
    async def insert(surveyquestion_data: SurveyQuestionBase):
        conn = await get_database()
        try:
            query = """
                INSERT INTO surveyquestions (surveyid, questionid)
                VALUES ($1, $2)
                RETURNING surveyid, questionid
            """
            async with conn.transaction():
                record = await conn.fetchrow(query, surveyquestion_data.surveyid, surveyquestion_data.questionid)
                return SurveyQuestionBase(**record)
        except Exception as e:
            raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, f"Failed to insert survey question: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def get_by_survey(surveyid: int):
        conn = await get_database()
        try:
            query = """
                SELECT q.id, q.title, q.scorefactor
                FROM surveyquestions sq
                JOIN question q ON sq.questionid = q.id
                WHERE sq.surveyid = $1
            """
            records = await conn.fetch(query, surveyid)
            return [SurveyQuestionBase(**record) for record in records]
        except Exception as e:
            raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, f"Failed to get questions for survey: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def get_by_question(questionid: int):
        conn = await get_database()
        try:
            query = """
                SELECT s.id, s.title
                FROM surveyquestions sq
                JOIN survey s ON sq.surveyid = s.id
                WHERE sq.questionid = $1
            """
            records = await conn.fetch(query, questionid)
            return [SurveyQuestionBase(**record) for record in records]
        except Exception as e:
            raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, f"Failed to get surveys for question: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def delete(surveyquestion_data: SurveyQuestionBase):
        surveyid = surveyquestion_data.surveyid
        questionid = surveyquestion_data.questionid

        conn = await get_database()
        try:
            query = """
                DELETE FROM surveyquestions
                WHERE surveyid = $1 AND questionid = $2
                RETURNING surveyid, questionid
            """
            async with conn.transaction():
                record = await conn.fetchrow(query, surveyid, questionid)
                if record:
                    return SurveyQuestionBase(**record)
                else:
                    raise HTTPException(HTTPStatus.NOT_FOUND, "Survey question not found")
        except asyncpg.ForeignKeyViolationError:
            raise HTTPException(HTTPStatus.CONFLICT, 
                                "Unable to delete survey question: related data exists in another table.")
        except asyncpg.PostgresError as e:            raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, f"Failed to delete survey question: {str(e)}")
        finally:
            await conn.close()
