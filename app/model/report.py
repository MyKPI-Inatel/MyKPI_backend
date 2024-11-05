from decimal import Decimal
from pydantic import BaseModel

class ReportBySurvey(BaseModel):
    question_id: int
    question_title: str
    survey_id: int
    average_score: Decimal
    scorefactor_multiplied: Decimal