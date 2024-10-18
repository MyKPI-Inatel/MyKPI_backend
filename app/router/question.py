from fastapi import APIRouter, HTTPException
from typing import List
from model.question import QuestionBase, QuestionCreate, QuestionUpdate
from service.question import Question as QuestionService

router = APIRouter()

@router.post(
    "", 
    response_model=QuestionBase, 
    summary="Create a new question", 
    description="This endpoint allows you to create a new question in the system."
)
async def create_question(question: QuestionCreate):
    new_question = await QuestionService.create_question(question)
    return new_question

@router.get(
    "", 
    response_model=List[QuestionBase], 
    summary="Retrieve all questions", 
    description="Retrieve a list of all questions in the system."
)
async def get_all_questions():
    questions = await QuestionService.get_all_questions()
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
