from http import HTTPStatus
import pytest
from httpx import ASGITransport, AsyncClient

from main import appServer

@pytest.mark.asyncio
@pytest.mark.quest
@pytest.mark.functional
async def test_api_create_question():
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        # Sample data for the question
        question_data = {
            "title": "Who are you?",
            "scorefactor": 2,
            "surveyid": 1
        }
        
        # Send a POST request to create a question
        response = await client.post("/api/v1/questions/", json=question_data)

        # Assert the response status code
        assert response.status_code == HTTPStatus.CREATED
        
        # Assert the returned data matches the expected format
        assert response.json() == {
            "id": 21,
            "title": "Who are you?",
            "scorefactor": 2
        }