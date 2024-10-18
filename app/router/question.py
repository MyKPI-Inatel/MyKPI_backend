from fastapi import APIRouter, HTTPException
from typing import List
from model.question import QuestionBase, QuestionCreate, QuestionUpdate
from service.question import Question as QuestionService

router = APIRouter()

@router.post("", response_model=QuestionBase)
async def create_question(question: QuestionCreate):
    new_question = await QuestionService.create_question(question)
    return new_question

@router.get("", response_model=List[QuestionBase])
async def get_all_questions():
    questions = await QuestionService.get_all_questions()
    return questions

@router.get("/{questionid}", response_model=QuestionBase)
async def get_question(questionid: int):
    question = await QuestionService.get_question(questionid)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.put("/{questionid}", response_model=QuestionBase)
async def update_question(questionid: int, question: QuestionUpdate):
    updated_question = await QuestionService.update_question(questionid, question)
    if updated_question is None:
        raise HTTPException(status_code=400, detail="Error updating question")
    return updated_question

@router.delete("/{questionid}")
async def delete_question(questionid: int):
    result = await QuestionService.delete_question(questionid)
    if not result:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted successfully"}
