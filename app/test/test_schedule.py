import pytest
from unittest.mock import patch, AsyncMock
from datetime import datetime
from model.survey import SurveyBase, SurveyCreate, SurveyUpdate
from dao.survey import SurveyDAO

@pytest.mark.asyncio
@patch("dao.survey.get_database", new_callable=AsyncMock)
async def test_get_survey(mock_get_database):
    # Arrange
    mock_conn = mock_get_database.return_value
    mock_conn.fetchrow.return_value = {
        "id": 1,
        "title": "Survey 1",
        "orgId": 1
    }

    # Act
    result = await SurveyDAO.get(1)

    # Assert
    assert result.id == 1
    assert result.title == "Survey 1"
    assert result.orgId == 1

@pytest.mark.asyncio
@patch("dao.survey.get_database", new_callable=AsyncMock)
async def test_get_all_surveys(mock_get_database):
    # Arrange
    mock_conn = mock_get_database.return_value
    mock_conn.fetch.return_value = [
        {
            "id": 1,
            "title": "Survey 1",
            "orgId": 1
        },
        {
            "id": 2,
            "title": "Survey 2",
            "orgId": 2
        }
    ]

    # Act
    result = await SurveyDAO.get_all()

    # Assert
    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].title == "Survey 1"
    assert result[1].id == 2
    assert result[1].title == "Survey 2"
