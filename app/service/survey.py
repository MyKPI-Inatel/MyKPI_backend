from model.survey import SurveyCreate, SurveyUpdate, SurveyBase
from dao.survey import SurveyDAO

class Survey:
    @staticmethod
    async def create_survey(survey_data: SurveyCreate) -> SurveyBase:
        new_survey_data = await SurveyDAO.insert(survey_data)
        return new_survey_data

    @staticmethod
    async def get_all_surveys() -> list[SurveyBase]:
        surveys_data = await SurveyDAO.get_all()
        return surveys_data

    @staticmethod
    async def get_survey(surveyid: int) -> SurveyBase:
        survey_data = await SurveyDAO.get(surveyid)
        return survey_data

    @staticmethod
    async def update_survey(surveyid: int, survey_data: SurveyUpdate) -> SurveyBase:
        updated_survey_data = await SurveyDAO.update(surveyid, survey_data)
        return updated_survey_data

    @staticmethod
    async def delete_survey(surveyid: int) -> bool:
        return await SurveyDAO.delete(surveyid)