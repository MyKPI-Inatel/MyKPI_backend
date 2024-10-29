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
