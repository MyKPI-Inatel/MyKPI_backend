from fastapi import APIRouter, Depends
from typing import List
from service.report import Report as ReportService
from fastapi import APIRouter
from service.user import User
from model.user import UserType
from internal.security import get_current_user, verify_permissions
from service.survey import Survey as SurveyService

router = APIRouter()

@router.get(
    "/{surveyid}", 
    response_model=List, 
    summary="Retrieve all reports", 
    description="Retrieve a list of all reports available."
)
async def get_reports(surveyid: int,
    current_user: User = Depends(get_current_user)):

    survey = await SurveyService.get_survey(surveyid)

    verify_permissions(current_user, UserType.orgadmin, {'orgid': survey.orgid})
    reports = await ReportService.get_report_by_surveyid(surveyid)
    return reports