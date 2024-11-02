from typing import List, Optional
from pydantic import BaseModel

class ReportBySurvey(BaseModel):
    question_id: int
    question_title: str
    survey_id: int
    average_score: int
    scorefactor_multiplied: int

