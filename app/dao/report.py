from fastapi import HTTPException
from dao.database import get_database
from model.report import ReportBySurvey

class ReportDAO:
    @staticmethod
    async def get_by_surveyid(surveyid: int):
        conn = await get_database()
        try:
            query = """
                SELECT 
                    q.id AS question_id,
                    q.title AS question_title,
                    qs.surveyid AS survey_id,
                    AVG(qs.score) AS average_score,
                    q.scorefactor * AVG(qs.score) AS scorefactor_multiplied
                FROM 
                    question q
                JOIN 
                    questionscore qs ON q.id = qs.questionid
                where 
                    qs.surveyid = $1
                GROUP BY 
                    q.id, q.title, qs.surveyid, q.scorefactor;
            """
            records = await conn.fetch(query, surveyid)
            return [ReportBySurvey(**record) for record in records]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get surveys: {str(e)}")
        finally:
            await conn.close()