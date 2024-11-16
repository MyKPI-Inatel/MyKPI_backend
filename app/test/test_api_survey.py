from http import HTTPStatus
import pytest, pytest_asyncio
from httpx import ASGITransport, AsyncClient

from dao.database import Database
from main import appServer

@pytest_asyncio.fixture()
async def reset_database():
    await Database.reset_database()

@pytest_asyncio.fixture
async def access_token_orgadmin():
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        login_data = {
            "username": "admin@inatel.br",
            "password": "senha"
        }
        response = await client.post("/api/v1/login", data=login_data)
        return response.json()["access_token"]

@pytest_asyncio.fixture
async def access_token_superadmin():
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        login_data = {
            "username": "admin@mykpi.online",
            "password": "senha"
        }
        response = await client.post("/api/v1/login", data=login_data)
        return response.json()["access_token"]

@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
async def test_api_create_survey(reset_database, access_token_orgadmin):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        survey_data = {"title": "Survey at Inatel", "orgid": 2}
        headers = {"Authorization": f"Bearer {access_token_orgadmin}"}
        
        response = await client.post("/api/v1/surveys/", json=survey_data, headers=headers)
        assert response.status_code == HTTPStatus.CREATED
        
        response_json = response.json()
        assert response_json["title"] == "Survey at Inatel"
        assert response_json["orgid"] == 2
        assert isinstance(response_json["id"], int)

@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
async def test_api_get_surveys(reset_database, access_token_superadmin):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {access_token_superadmin}"}
        response = await client.get("/api/v1/surveys/", headers=headers)
        assert response.status_code == HTTPStatus.OK
        
        response_json = response.json()
        assert isinstance(response_json, list)

@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
async def test_api_get_survey(reset_database, access_token_orgadmin):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {access_token_orgadmin}"}
        survey_data = {"title": "Survey at Inatel", "orgid": 2}
        create_response = await client.post("/api/v1/surveys/", json=survey_data, headers=headers)
        survey_id = create_response.json()["id"]

        response = await client.get(f"/api/v1/surveys/{survey_id}", headers=headers)
        assert response.status_code == HTTPStatus.OK
        
        response_json = response.json()
        assert response_json["title"] == "Survey at Inatel"
        assert response_json["orgid"] == 2

@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
async def test_api_get_surveys_by_org(reset_database, access_token_orgadmin):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {access_token_orgadmin}"}
        survey_data = {"title": "Survey at Inatel", "orgid": 2}
        await client.post("/api/v1/surveys/", json=survey_data, headers=headers)

        response = await client.get("/api/v1/surveys/org/2", headers=headers)
        assert response.status_code == HTTPStatus.OK
        
        response_json = response.json()
        assert isinstance(response_json, list)
        assert any(survey["orgid"] == 2 for survey in response_json)
