from http import HTTPStatus
import pytest, pytest_asyncio
from httpx import ASGITransport, AsyncClient

from dao.database import Database

from main import appServer

@pytest_asyncio.fixture()
async def reset_database():
    await Database.reset_database()

@pytest_asyncio.fixture
async def access_token():
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        login_data = {
            "username": "admin@inatel.br",
            "password": "senha"
        }
        response = await client.post("/api/v1/login", data=login_data)
        return response.json()["access_token"]

@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
async def test_api_create_survey(reset_database, access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        # Sample data for the survey
        survey_data = {
            "title": "Survey at Inatel",
            "orgid": 2
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = await client.post("/api/v1/surveys/", json=survey_data, headers=headers)

        # Assert the response status code
        assert response.status_code == HTTPStatus.CREATED
        
        # Assert the returned data matches the expected format
        response_json = response.json()
        assert response_json["title"] == "Survey at Inatel"
        assert response_json["orgid"] == 2
        assert isinstance(response_json["id"], int)
