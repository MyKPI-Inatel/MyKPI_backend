import pytest
from unittest.mock import AsyncMock
from service.surveyquestion import SurveyQuestion
from model.surveyquestion import SurveyQuestionCreate, SurveyQuestionBase
from dao.surveyquestion import SurveyQuestionDAO

@pytest.mark.asyncio
@pytest.mark.survquest
@pytest.mark.unit
async def test_svc_create_surveyquestion(mocker):
    # Mock input and expected return values
    surveyquestion_data = SurveyQuestionCreate(surveyid=2, questionid=3)
    expected_return = SurveyQuestionBase(surveyid=2, questionid=3)

    # Mock the insert method of the DAO
    mocker.patch.object(SurveyQuestionDAO, 'insert', new_callable=AsyncMock, return_value=expected_return)

    # Call the function we're testing
    result = await SurveyQuestion.create_surveyquestion(surveyquestion_data)

    # Asserts that the DAO's insert method was called with the correct input
    SurveyQuestionDAO.insert.assert_called_once_with(surveyquestion_data)

    # Asserts that the result is as expected
    assert result == expected_return


@pytest.mark.asyncio
@pytest.mark.survquest
@pytest.mark.unit
async def test_svc_get_surveyquestion_by_question(mocker):
    # Mock input and expected return values
    questionid = 5
    expected_return = [SurveyQuestionBase(surveyid=2, questionid=questionid)]

    # Mock the get method of the DAO
    mocker.patch.object(SurveyQuestionDAO, 'get_by_question', new_callable=AsyncMock, return_value=expected_return)

    # Call the function we're testing
    result = await SurveyQuestion.get_by_question(questionid)

    # Asserts that the DAO's get method was called with the correct input
    SurveyQuestionDAO.get_by_question.assert_called_once_with(questionid)

    # Asserts that the result is as expected
    assert result == expected_return


@pytest.mark.asyncio
@pytest.mark.survquest
@pytest.mark.unit
async def test_svc_get_surveyquestion_by_survey(mocker):
    # Mock input and expected return values
    surveyid = 1
    expected_return = [SurveyQuestionBase(surveyid=surveyid, questionid=2),
                       SurveyQuestionBase(surveyid=surveyid, questionid=3),
                       SurveyQuestionBase(surveyid=surveyid, questionid=4)]

    # Mock the get method of the DAO
    mocker.patch.object(SurveyQuestionDAO, 'get_by_survey', new_callable=AsyncMock, return_value=expected_return)

    # Call the function we're testing
    result = await SurveyQuestion.get_by_survey(surveyid)

    # Asserts that the DAO's get method was called with the correct input
    SurveyQuestionDAO.get_by_survey.assert_called_once_with(surveyid)

    # Asserts that the result is as expected
    assert result == expected_return


@pytest.mark.asyncio
@pytest.mark.survquest
@pytest.mark.unit
async def test_svc_delete_surveyquestion(mocker):
    # Mock input and expected return values
    surveyquestionid = 1
    expected_return = True

    # Mock the delete method of the DAO
    mocker.patch.object(SurveyQuestionDAO, 'delete', new_callable=AsyncMock, return_value=expected_return)

    # Call the function we're testing
    result = await SurveyQuestion.delete_surveyquestion(surveyquestionid)

    # Asserts that the DAO's delete method was called with the correct input
    SurveyQuestionDAO.delete.assert_called_once_with(surveyquestionid)

    # Asserts that the result is as expected
    assert result == expected_return