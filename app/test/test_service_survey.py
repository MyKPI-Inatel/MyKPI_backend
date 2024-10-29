import pytest
from unittest.mock import AsyncMock
from service.survey import Survey
from model.survey import SurveyCreate, SurveyBase
from dao.survey import SurveyDAO

@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.unit
async def test_svc_create_survey(mocker):
    # Mock input and expected return values
    survey_data = SurveyCreate(title="Survey at Inatel", orgid=1)
    expected_return = SurveyBase(id=1, title="Survey at Inatel", orgid=1)

    # Mock the insert method of the DAO
    mocker.patch.object(SurveyDAO, 'insert', new_callable=AsyncMock, return_value=expected_return)

    # Call the function we're testing
    result = await Survey.create_survey(survey_data)

    # Asserts that the DAO's insert method was called with the correct input
    SurveyDAO.insert.assert_called_once_with(survey_data)

    # Asserts that the result is as expected
    assert result == expected_return