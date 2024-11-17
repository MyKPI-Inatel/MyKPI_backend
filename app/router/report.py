from http import HTTPStatus
from fastapi import APIRouter, Depends
from typing import List

from internal.security import get_current_user, verify_permissions

from model.user import UserType, CurrentUser

from service.report import Report
from service.survey import Survey

router = APIRouter()

@router.get(
    "/{surveyid}",
    status_code=HTTPStatus.OK,
    response_model=List, 
    summary="Retrieve all reports", 
    description="Retrieve a list of all reports available."
)
async def get_reports(surveyid: int,
    current_user: CurrentUser = Depends(get_current_user)
):

    survey = await Survey.get_survey(surveyid)

    verify_permissions(current_user, UserType.orgadmin, {'orgid': survey.orgid})
    return await Report.get_report_by_surveyid(surveyid)