from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from internal.security import get_current_user, verify_permissions

from model.survey import SurveyBase, SurveyCreate, SurveyUpdate, SurveyResponse
from model.user import UserType, CurrentUser

from service.survey import Survey

router = APIRouter()

@router.post("/",
    status_code=HTTPStatus.CREATED,
    response_model=SurveyBase, 
    summary="Create a new survey", 
    description="This endpoint allows you to create a new survey."
)
async def create_survey(survey: SurveyCreate,
    current_user: CurrentUser = Depends(get_current_user)
):
    verify_permissions(current_user, UserType.orgadmin, {'orgid': survey.orgid})

    return await Survey.create_survey(survey)

@router.get("/",
    status_code=HTTPStatus.OK,
    response_model=List[SurveyBase], 
    summary="Retrieve all surveys", 
    description="Retrieve a list of all surveys available."
)
async def get_surveys(
    current_user: CurrentUser = Depends(get_current_user)
):
    verify_permissions(current_user, UserType.superadmin)

    return await Survey.get_all_surveys()

@router.get(
    "/{surveyid}",
    status_code=HTTPStatus.OK,
    response_model=SurveyBase, 
    summary="Retrieve a survey by ID", 
    description="Retrieve a specific survey by its ID."
)
async def get_survey(surveyid: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    survey = await Survey.get_survey(surveyid)
    
    verify_permissions(current_user, UserType.employee, {'orgid': survey.orgid})
    
    return survey

@router.get(
    "/org/{orgid}",
    status_code=HTTPStatus.OK,
    response_model=List[SurveyBase],
    summary="Retrieve all surveys by organization ID",
    description="Retrieve a list of all surveys associated with a specific organization ID."
)
async def get_surveys_by_org(orgid: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    verify_permissions(current_user, UserType.employee, {'orgid': orgid})

    return await Survey.get_survey_by_org(orgid)

@router.put(
    "/{surveyid}",
    status_code=HTTPStatus.OK,
    response_model=SurveyBase, 
    summary="Update a survey", 
    description="Update the details of a specific survey by its ID."
)
async def update_survey(surveyid: int, survey: SurveyUpdate,
    current_user: CurrentUser = Depends(get_current_user)
):
    survey_data = await Survey.get_survey(surveyid)

    verify_permissions(current_user, UserType.orgadmin, {'orgid': survey_data.orgid})

    result = await Survey.update_survey(surveyid, survey)
    if not result:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Survey not found')
    return result

@router.delete(
    "/{surveyid}",
    status_code=HTTPStatus.OK,
    summary="Delete a survey", 
    description="Delete a specific survey by its ID."
)
async def delete_survey(surveyid: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    survey = await Survey.get_survey(surveyid)
    
    verify_permissions(current_user, UserType.orgadmin, {'orgid': survey.orgid})

    result = await Survey.delete_survey(surveyid)
    if not result:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Survey not found')
    return {"message": "Survey deleted successfully"}

@router.get(
    "/unresponded/{employee_id}",
    status_code=HTTPStatus.OK,
    response_model=List[SurveyResponse],
    summary="Retrieve all unresponded surveys",
    description="Retrieve a list of all surveys that have not been responded by the user."
)
async def get_unresponded_surveys(employee_id: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    verify_permissions(current_user, UserType.employee, {'id': employee_id})

    return await Survey.get_unresponded_surveys(employee_id)
