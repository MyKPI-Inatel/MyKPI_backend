from fastapi import APIRouter, HTTPException
from typing import List
from model.surveyquestion import SurveyQuestionBase
from model.question import QuestionBase, QuestionCreate, QuestionUpdate
from service.question import Question as QuestionService
from service.surveyquestion import SurveyQuestion as SurveyQuestionService

router = APIRouter()

@router.post(
    "/", 
    response_model=QuestionBase,
    summary="Create a new question",
    description="This endpoint allows you to create a new question."
)
async def create_question(question: QuestionCreate):
    new_question = await QuestionService.create_question(question)
    return new_question

@router.post(
    "/{questionid}/survey/{surveyid}",
    response_model=SurveyQuestionBase,
    summary="Associate a question with a survey",
    description="This endpoint allows you to associate a question with a survey."
)
async def sync_question_with_survey(questionid: int, surveyid: int):
    surveyquestion_data = SurveyQuestionBase(surveyid=surveyid, questionid=questionid)
    survey_question = await SurveyQuestionService.create_surveyquestion(surveyquestion_data)
    return survey_question

@router.get(
    "/",
    response_model=List[QuestionBase],
    summary="Retrieve all questions",
    description="Retrieve a list of all questions."
)
async def get_all_questions():
    questions = await QuestionService.get_all_questions()
    return questions

@router.get(
    "/survey/{surveyid}",
    response_model=List[QuestionBase],
    summary="Retrieve all questions for a specific survey",
    description="Retrieve a list of all questions associated with a specific survey."
)
async def get_by_survey(surveyid: int):
    questions = await QuestionService.get_by_survey(surveyid)
    return questions
    

@router.get(
    "/{questionid}",
    response_model=QuestionBase,
    summary="Retrieve a specific question",
    description="Retrieve a question by its ID."
)
async def get_question(questionid: int):
    question = await QuestionService.get_question(questionid)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.put(
    "/{questionid}",
    response_model=QuestionBase,
    summary="Update a specific question",
    description="Update a question by its ID with the provided data."
)
async def update_question(questionid: int, question: QuestionUpdate):
    updated_question = await QuestionService.update_question(questionid, question)
    if updated_question is None:
        raise HTTPException(status_code=400, detail="Error updating question")
    return updated_question

@router.delete(
    "/{questionid}",
    summary="Delete a specific question",
    description="Delete a question by its ID."
)
async def delete_question(questionid: int):
    result = await QuestionService.delete_question(questionid)
    if not result:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted successfully"}
