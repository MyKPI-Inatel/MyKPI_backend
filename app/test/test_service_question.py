import pytest
from unittest.mock import AsyncMock
from service.question import Question
from model.question import QuestionCreate, QuestionBase
from dao.question import QuestionDAO
from model.surveyquestion import SurveyQuestionBase
from dao.surveyquestion import SurveyQuestionDAO

@pytest.mark.asyncio
@pytest.mark.quest
@pytest.mark.unit
async def test_svc_create_question(mocker):
    # Mock input and expected return values
    survey_id = 1

    question_data = QuestionCreate(title="What is your name?", scorefactor=1, surveyid=survey_id)
    expected_quesion_return = QuestionBase(id=1, title="What is your name?", scorefactor=1, surveyid=survey_id)

    expected_surveyquestion_return = SurveyQuestionBase(surveyid=survey_id, questionid=1)

    # Mock the insert method of the DAO
    mocker.patch.object(QuestionDAO, 'insert', new_callable=AsyncMock, return_value=expected_quesion_return)

    # Mock the insert method of the DAO
    mocker.patch.object(SurveyQuestionDAO, 'insert', new_callable=AsyncMock, return_value=expected_surveyquestion_return)

    # Call the function we're testing
    result = await Question.create_question(question_data)

    # Asserts that the DAO's insert method was called with the correct input
    QuestionDAO.insert.assert_called_once_with(question_data)

    # Asserts that the DAO's insert method was called with the correct input
    SurveyQuestionDAO.insert.assert_called_once_with(survey_id, expected_quesion_return.id)

    # Asserts that the result is as expected
    assert result == expected_quesion_return