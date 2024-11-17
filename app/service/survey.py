from dao.survey import SurveyDAO

from model.survey import SurveyCreate, SurveyUpdate, SurveyBase, SurveyResponse

class Survey:
    @staticmethod
    async def create_survey(survey_data: SurveyCreate) -> SurveyBase:
        return await SurveyDAO.insert(survey_data)

    @staticmethod
    async def get_all_surveys() -> list[SurveyBase]:
        return await SurveyDAO.get_all()

    @staticmethod
    async def get_survey(surveyid: int) -> SurveyBase:
        return await SurveyDAO.get(surveyid)
    
    @staticmethod
    async def get_survey_by_org(orgid: int) -> list[SurveyBase]:
        return await SurveyDAO.get_by_org(orgid)

    @staticmethod
    async def update_survey(surveyid: int, survey_data: SurveyUpdate) -> SurveyBase:
        return await SurveyDAO.update(surveyid, survey_data)

    @staticmethod
    async def delete_survey(surveyid: int) -> bool:
        return await SurveyDAO.delete(surveyid)
    
    @staticmethod
    async def get_unresponded_surveys(employee_id: int) -> list[SurveyResponse]:
        return await SurveyDAO.get_unresponded_surveys(employee_id)