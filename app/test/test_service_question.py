import pytest
from unittest.mock import AsyncMock
from service.question import Question
from model.question import QuestionCreate, QuestionBase, QuestionUpdate
from dao.question import QuestionDAO
from model.surveyquestion import SurveyQuestionBase
from service.surveyquestion import SurveyQuestion

@pytest.mark.asyncio
@pytest.mark.quest
@pytest.mark.unit
async def test_svc_create_question(mocker):
    # Mock input and expected return values
    survey_id = 1
    question_data = QuestionCreate(title="What is your name?", scorefactor=1, surveyid=survey_id)
    expected_question_return = QuestionBase(id=1, title="What is your name?", scorefactor=1, surveyid=survey_id)
    expected_surveyquestion_data = SurveyQuestionBase(surveyid=survey_id, questionid=expected_question_return.id)

    # Mock the insert method of the QuestionDAO
    mocker.patch.object(QuestionDAO, 'insert', new_callable=AsyncMock, return_value=expected_question_return)

    # Mock the create_surveyquestion method of the SurveyQuestion
    mocker.patch.object(SurveyQuestion, 'create_surveyquestion', new_callable=AsyncMock)

    # Call the function we're testing
    result = await Question.create_question(question_data)

    # Assert that QuestionDAO's insert method was called with the correct input
    QuestionDAO.insert.assert_called_once_with(question_data)

    # Assert that SurveyQuestion's create_surveyquestion method was called with the correct data
    SurveyQuestion.create_surveyquestion.assert_called_once_with(expected_surveyquestion_data)

    # Assert that the result is as expected
    assert result == expected_question_return



@pytest.mark.asyncio
@pytest.mark.quest
@pytest.mark.unit
async def test_svc_get_question(mocker):
    # Mock input and expected return values
    questionid = 1
    expected_return = QuestionBase(id=1, title="What is your name?", scorefactor=1, surveyid=1)

    # Mock the get method of the DAO
    mocker.patch.object(QuestionDAO, 'get', new_callable=AsyncMock, return_value=expected_return)

    # Call the function we're testing
    result = await Question.get_question(questionid)

    # Asserts that the DAO's get method was called with the correct input
    QuestionDAO.get.assert_called_once_with(questionid)

    # Asserts that the result is as expected
    assert result == expected_return


@pytest.mark.asyncio
@pytest.mark.quest
@pytest.mark.unit
async def test_svc_get_all_questions(mocker):
    # Mock expected return values
    expected_return = [QuestionBase(id=1, title="What is your name?", scorefactor=1, surveyid=1),
                       QuestionBase(id=2, title="What is your age?", scorefactor=1, surveyid=1),
                       QuestionBase(id=3, title="What is your gender?", scorefactor=1, surveyid=1)]

    # Mock the get_all method of the DAO
    mocker.patch.object(QuestionDAO, 'get_all', new_callable=AsyncMock, return_value=expected_return)

    # Call the function we're testing
    result = await Question.get_all_questions()

    # Asserts that the DAO's get_all method was called
    QuestionDAO.get_all.assert_called_once()

    # Asserts that the result is as expected
    assert result == expected_return


@pytest.mark.asyncio
@pytest.mark.quest
@pytest.mark.unit
async def test_svc_update_question(mocker):
    # Mock input and expected return values
    questionid = 1
    question_data = QuestionUpdate(title="What is your name?", scorefactor=1, surveyid=1)
    expected_return = QuestionBase(id=1, title="What is your name?", scorefactor=1, surveyid=1)

    # Mock the update method of the DAO
    mocker.patch.object(QuestionDAO, 'update', new_callable=AsyncMock, return_value=expected_return)

    # Call the function we're testing
    result = await Question.update_question(questionid, question_data)

    # Asserts that the DAO's update method was called with the correct input
    QuestionDAO.update.assert_called_once_with(questionid, question_data)

    # Asserts that the result is as expected
    assert result == expected_return


@pytest.mark.asyncio
@pytest.mark.quest
@pytest.mark.unit
async def test_svc_delete_question(mocker):
    # Mock input and expected return values
    questionid = 1
    expected_return = True

    # Mock the delete method of the DAO
    mocker.patch.object(QuestionDAO, 'delete', new_callable=AsyncMock, return_value=expected_return)

    # Call the function we're testing
    result = await Question.delete_question(questionid)

    # Asserts that the DAO's delete method was called with the correct input
    QuestionDAO.delete.assert_called_once_with(questionid)

    # Asserts that the result is as expected
    assert result == expected_return