from dao.question import QuestionDAO

from model.surveyquestion import SurveyQuestionBase
from model.question import QuestionCreate, QuestionToScore, QuestionUpdate, QuestionBase

from service.surveyquestion import SurveyQuestion

class Question:
    @staticmethod
    async def create_question(question_data: QuestionCreate) -> QuestionBase:
        new_question_data = await QuestionDAO.insert(question_data) # there's no surveyid yet

        surveyquestion_data = SurveyQuestionBase(
            surveyid=question_data.surveyid,
            questionid=new_question_data.id
        )

        new_question_data.surveyid = question_data.surveyid

        await SurveyQuestion.create_surveyquestion(surveyquestion_data)
        
        return new_question_data

    @staticmethod
    async def get_all_questions() -> list[QuestionBase]:
        questions_data = await QuestionDAO.get_all()
        return questions_data

    @staticmethod
    async def get_question(questionid: int) -> QuestionBase:
        question_data = await QuestionDAO.get(questionid)
        return question_data
    
    @staticmethod
    async def get_by_survey(surveyid: int) -> list[QuestionBase]:
        questions_data = await QuestionDAO.get_by_survey(surveyid)
        return questions_data

    @staticmethod
    async def update_question(questionid: int, question_data: QuestionUpdate) -> QuestionBase:
        updated_question_data = await QuestionDAO.update(questionid, question_data)
        return updated_question_data

    @staticmethod
    async def delete_question(questionid: int) -> bool:
        return await QuestionDAO.delete(questionid)
    
    @staticmethod
    async def add_question_score(questionscore: QuestionToScore) -> bool:
        return await QuestionDAO.add_question_score(questionscore)
