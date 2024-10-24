from fastapi import APIRouter, HTTPException
from typing import List
from model.survey import SurveyBase, SurveyCreate, SurveyUpdate, SurveyResponse
from service.survey import Survey as SurveyService

router = APIRouter()

@router.post(
    "/", 
    response_model=SurveyBase, 
    summary="Create a new survey", 
    description="This endpoint allows you to create a new survey."
)
async def create_survey(survey: SurveyCreate):
    return await SurveyService.create_survey(survey)

@router.get(
    "/", 
    response_model=List[SurveyBase], 
    summary="Retrieve all surveys", 
    description="Retrieve a list of all surveys available."
)
async def get_surveys():
    surveys = await SurveyService.get_all_surveys()
    return surveys

@router.get(
    "/{surveyid}", 
    response_model=SurveyBase, 
    summary="Retrieve a survey by ID", 
    description="Retrieve a specific survey by its ID."
)
async def get_survey(surveyid: int):
    survey = await SurveyService.get_survey(surveyid)
    if survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey

@router.get(
    "/org/{orgid}",
    response_model=List[SurveyBase],
    summary="Retrieve all surveys by organization ID",
    description="Retrieve a list of all surveys associated with a specific organization ID."
)
async def get_surveys_by_org(orgid: int):
    surveys = await SurveyService.get_survey_by_org(orgid)
    return surveys

@router.put(
    "/{surveyid}", 
    response_model=SurveyBase, 
    summary="Update a survey", 
    description="Update the details of a specific survey by its ID."
)
async def update_survey(surveyid: int, survey: SurveyUpdate):
    result = await SurveyService.update_survey(surveyid, survey)
    if not result:
        raise HTTPException(status_code=404, detail="Survey not found")
    return result

@router.delete(
    "/{surveyid}", 
    summary="Delete a survey", 
    description="Delete a specific survey by its ID."
)
async def delete_survey(surveyid: int):
    result = await SurveyService.delete_survey(surveyid)
    if not result:
        raise HTTPException(status_code=404, detail="Survey not found")
    return {"message": "Survey deleted successfully"}

# rota para pesquisar as surveys não respondidas pelo usuario
@router.get(
    "/unresponded/{employee_id}",
    response_model=List[SurveyResponse],
    summary="Retrieve all unresponded surveys",
    description="Retrieve a list of all surveys that have not been responded by the user."
)
async def get_unresponded_surveys(employee_id: int):
    surveys = await SurveyService.get_unresponded_surveys(employee_id)
    return surveys
