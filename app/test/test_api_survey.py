from fastapi.security import OAuth2PasswordRequestForm
import pytest
from httpx import ASGITransport, AsyncClient
from dao.database import Database
from main import appServer
import pytest_asyncio

@pytest_asyncio.fixture()
async def reset_database():
    await Database.reset_database()

@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
async def test_api_create_survey(reset_database):
    
    access_token = None

    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        login_data = {
            "username": "admin@mykpi.online",
            "password": "senha"
        }

        response = await client.post("/api/v1/login", data=login_data)
        access_token = response.json()["access_token"]

    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        # Sample data for the survey
        survey_data = {
            "title": "Survey at Inatel",
            "orgid": 1
        }
        
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.post("/api/v1/surveys/", json=survey_data, headers=headers)

        # Assert the response status code
        assert response.status_code == 200
        
        # Assert the returned data matches the expected format
        assert response.json() == {
            "id": 5,
            "title": "Survey at Inatel",
            "orgid": 1,
            "questions": None
        }