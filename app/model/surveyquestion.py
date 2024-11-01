from pydantic import BaseModel

class SurveyQuestionBase(BaseModel):
    surveyid: int
    questionid: int

class SurveyQuestionCreate(BaseModel):
    surveyid: int
    questionid: int