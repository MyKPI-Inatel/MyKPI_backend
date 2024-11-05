from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from internal.security import get_current_user, verify_permissions

from model.question import QuestionBase, QuestionCreate, QuestionToScore, QuestionUpdate
from model.surveyquestion import SurveyQuestionBase
from model.user import UserType

from service.question import Question
from service.surveyquestion import SurveyQuestion
from service.user import User
from service.survey import Survey

router = APIRouter()

@router.post(
    "/", 
    response_model=QuestionBase,
    summary="Create a new question",
    description="This endpoint allows you to create a new question."
)
async def create_question(question: QuestionCreate):
    new_question = await Question.create_question(question)
    return new_question

@router.post(
    "/{questionid}/survey/{surveyid}",
    response_model=SurveyQuestionBase,
    summary="Associate a question with a survey",
    description="This endpoint allows you to associate a question with a survey."
)
async def sync_question_with_survey(questionid: int, surveyid: int):
    surveyquestion_data = SurveyQuestionBase(surveyid=surveyid, questionid=questionid)
    survey_question = await SurveyQuestion.create_surveyquestion(surveyquestion_data)
    return survey_question

@router.get(
    "/",
    response_model=List[QuestionBase],
    summary="Retrieve all questions",
    description="Retrieve a list of all questions."
)
async def get_all_questions():
    questions = await Question.get_all_questions()
    return questions

@router.get(
    "/survey/{surveyid}",
    response_model=List[QuestionBase],
    summary="Retrieve all questions for a specific survey",
    description="Retrieve a list of all questions associated with a specific survey."
)
async def get_by_survey(surveyid: int):
    questions = await Question.get_by_survey(surveyid)
    return questions
    

@router.get(
    "/{questionid}",
    response_model=QuestionBase,
    summary="Retrieve a specific question",
    description="Retrieve a question by its ID."
)
async def get_question(questionid: int):
    question = await Question.get_question(questionid)
    if question is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Question not found")
    return question

@router.put(
    "/{questionid}",
    response_model=QuestionBase,
    summary="Update a specific question",
    description="Update a question by its ID with the provided data."
)
async def update_question(questionid: int, question: QuestionUpdate):
    updated_question = await Question.update_question(questionid, question)
    if updated_question is None:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Error updating question")
    return updated_question

@router.delete(
    "/{questionid}",
    summary="Delete a specific question",
    description="Delete a question by its ID."
)
async def delete_question(questionid: int):
    result = await Question.delete_question(questionid)
    if not result:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Question not found")
    return {"message": "Question deleted successfully"}

@router.post(
    "/respond/",
    summary="Submit responses to questions",
    description="Submit responses to questions."
)
async def submit_responses(questionscores: QuestionToScore,
                           current_user: User = Depends(get_current_user)):
    survey_data = await Survey.get_survey(questionscores.surveyid)

    verify_permissions(current_user, UserType.employee, {'orgid': survey_data.orgid, 'id': questionscores.employeeid})

    result = await Question.add_question_score(questionscores)
    return result