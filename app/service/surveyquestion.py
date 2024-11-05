from dao.surveyquestion import SurveyQuestionDAO

from model.surveyquestion import SurveyQuestionCreate, SurveyQuestionBase

class SurveyQuestion:
    @staticmethod
    async def create_surveyquestion(surveyquestion_data: SurveyQuestionCreate) -> SurveyQuestionBase:
        new_surveyquestion_data = await SurveyQuestionDAO.insert(surveyquestion_data)
        return new_surveyquestion_data

    @staticmethod
    async def get_by_survey(surveyid: int) -> SurveyQuestionBase:
        surveyquestion_data = await SurveyQuestionDAO.get_by_survey(surveyid)
        return surveyquestion_data
    
    @staticmethod
    async def get_by_question(questionid: int) -> SurveyQuestionBase:
        surveyquestion_data = await SurveyQuestionDAO.get_by_question(questionid)
        return surveyquestion_data

    @staticmethod
    async def delete_surveyquestion(surveyquestion_data: SurveyQuestionBase) -> bool:
        return await SurveyQuestionDAO.delete(surveyquestion_data)
