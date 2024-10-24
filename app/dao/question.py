from fastapi import HTTPException
from dao.database import get_database
from model.question import QuestionCreate, QuestionUpdate, QuestionBase
import asyncpg

class QuestionDAO:
    @staticmethod
    async def insert(question: QuestionCreate):
        conn = await get_database()
        try:
            query = """
                INSERT INTO question (title, scorefactor)
                VALUES ($1, $2)
                RETURNING id, title, scorefactor
            """
            async with conn.transaction():
                record = await conn.fetchrow(query, question.title, question.scorefactor)
                return QuestionBase(**record)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to insert question: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def get_all():
        conn = await get_database()
        try:
            query = """
                SELECT q.id, q.title, q.scorefactor, sq.surveyid
                FROM question q
                LEFT JOIN surveyquestions sq
                ON sq.questionid = q.id
                ORDER BY q.id
            """
            records = await conn.fetch(query)
            return [QuestionBase(**record) for record in records]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get questions: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def get(questionid: int):
        conn = await get_database()
        try:
            query = """
                SELECT q.id, q.title, q.scorefactor, sq.surveyid
                FROM question q
                LEFT JOIN surveyquestions sq
                ON sq.questionid = q.id
                WHERE q.id = $1
            """
            record = await conn.fetchrow(query, questionid)
            if record:
                return QuestionBase(**record)
            else:
                raise HTTPException(status_code=404, detail="Question not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get question: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def get_by_survey(surveyid: int):
        conn = await get_database()
        try:
            query = """
                SELECT q.id, q.title, q.scorefactor, sq.surveyid
                FROM question q
                LEFT JOIN surveyquestions sq
                ON sq.questionid = q.id
                WHERE sq.surveyid = $1
                ORDER BY q.id
            """
            records = await conn.fetch(query, surveyid)
            return [QuestionBase(**record) for record in records]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get questions for survey: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def update(questionid: int, question: QuestionUpdate):
        conn = await get_database()
        try:
            update_data = question.dict(exclude_unset=True)
            set_clause = ", ".join([f"{key} = ${i+2}" for i, key in enumerate(update_data.keys())])
            query = f"""
                UPDATE question SET {set_clause} WHERE id = $1
                RETURNING id, title, scorefactor
            """
            values = [questionid] + list(update_data.values())
            async with conn.transaction():
                record = await conn.fetchrow(query, *values)
                if record:
                    return QuestionBase(**record)
                else:
                    raise HTTPException(status_code=404, detail="Question not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update question: {str(e)}")
        finally:
            await conn.close()

    @staticmethod
    async def delete(questionid: int):
        conn = await get_database()
        try:
            query = """
                DELETE FROM question WHERE id = $1
                RETURNING id
            """
            async with conn.transaction():
                record = await conn.fetchrow(query, questionid)
                if record:
                    return True
                else:
                    raise HTTPException(status_code=404, detail="Question not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete question: {str(e)}")
        finally:
            await conn.close()