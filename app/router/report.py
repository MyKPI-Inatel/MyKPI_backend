from fastapi import APIRouter
from typing import List
from service.report import Report as ReportService
from fastapi import APIRouter

router = APIRouter()

@router.get(
    "/{surveyid}", 
    response_model=List, 
    summary="Retrieve all reports", 
    description="Retrieve a list of all reports available."
)
async def get_reports(surveyid: int):
    reports = await ReportService.get_report_by_surveyid(surveyid)
    return reports