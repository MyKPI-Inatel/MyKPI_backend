from fastapi import APIRouter, HTTPException
from typing import List
from model.survey import SurveyBase, SurveyCreate, SurveyUpdate
from service.survey import Survey as SurveyService

router = APIRouter()

@router.post("/", response_model=SurveyBase)
async def create_survey(survey: SurveyCreate):
    return await SurveyService.create_survey(survey)

@router.get("/", response_model=List[SurveyBase])
async def get_surveys():
    surveys = await SurveyService.get_all_surveys()
    return surveys

@router.get("/{surveyid}", response_model=SurveyBase)
async def get_survey(surveyid: int):
    survey = await SurveyService.get_survey(surveyid)
    if survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey

@router.put("/{surveyid}", response_model=SurveyBase)
async def update_survey(surveyid: int, survey: SurveyUpdate):
    result = await SurveyService.update_survey(surveyid, survey)
    if not result:
        raise HTTPException(status_code=404, detail="Survey not found")
    return result

@router.delete("/{surveyid}")
async def delete_survey(surveyid: int):
    result = await SurveyService.delete_survey(surveyid)
    if not result:
        raise HTTPException(status_code=404, detail="Survey not found")
    return {"message": "Survey deleted successfully"}