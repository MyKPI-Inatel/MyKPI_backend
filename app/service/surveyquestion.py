from dao.surveyquestion import SurveyQuestionDAO

from model.surveyquestion import SurveyQuestionCreate, SurveyQuestionBase

class SurveyQuestion:
    @staticmethod
    async def create_surveyquestion(surveyquestion_data: SurveyQuestionCreate) -> SurveyQuestionBase:
        return await SurveyQuestionDAO.insert(surveyquestion_data)

    @staticmethod
    async def get_by_survey(surveyid: int) -> SurveyQuestionBase:
        return await SurveyQuestionDAO.get_by_survey(surveyid)
    
    @staticmethod
    async def get_by_question(questionid: int) -> SurveyQuestionBase:
        return await SurveyQuestionDAO.get_by_question(questionid)

    @staticmethod
    async def delete_surveyquestion(surveyquestion_data: SurveyQuestionBase) -> bool:
        return await SurveyQuestionDAO.delete(surveyquestion_data)
