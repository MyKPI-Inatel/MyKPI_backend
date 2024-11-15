from dao.report import ReportDAO

from model.report import ReportBySurvey

class Report:
    @staticmethod
    async def get_report_by_surveyid(surveyid: int) -> list[ReportBySurvey]:
        return await ReportDAO.get_by_surveyid(surveyid)