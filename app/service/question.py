from dao.question import QuestionDAO

from model.surveyquestion import SurveyQuestionBase
from model.question import QuestionCreate, QuestionToScore, QuestionUpdate, QuestionBase

from service.surveyquestion import SurveyQuestion

class Question:
    @staticmethod
    async def create_question(question_data: QuestionCreate) -> QuestionBase:
        return await QuestionDAO.insert(question_data)

    @staticmethod
    async def get_all_questions() -> list[QuestionBase]:
        return await QuestionDAO.get_all()

    @staticmethod
    async def get_question(questionid: int) -> QuestionBase:
        return await QuestionDAO.get(questionid)
    
    @staticmethod
    async def get_by_survey(surveyid: int) -> list[QuestionBase]:
        return await QuestionDAO.get_by_survey(surveyid)

    @staticmethod
    async def update_question(questionid: int, question_data: QuestionUpdate) -> QuestionBase:
        return await QuestionDAO.update(questionid, question_data)

    @staticmethod
    async def delete_question(questionid: int) -> bool:
        return await QuestionDAO.delete(questionid)
    
    @staticmethod
    async def add_question_score(questionscore: QuestionToScore) -> bool:
        return await QuestionDAO.add_question_score(questionscore)
