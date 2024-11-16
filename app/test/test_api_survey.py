from http import HTTPStatus
import pytest, pytest_asyncio
from httpx import ASGITransport, AsyncClient

from main import appServer

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
async def test_api_create_survey(access_token_orgadmin):
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
async def test_api_get_surveys(access_token_superadmin):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {access_token_superadmin}"}
        response = await client.get("/api/v1/surveys/", headers=headers)
        assert response.status_code == HTTPStatus.OK
        
        response_json = response.json()
        assert isinstance(response_json, list)

@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
async def test_api_get_survey(access_token_orgadmin):
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
async def test_api_get_surveys_by_org(access_token_orgadmin):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {access_token_orgadmin}"}
        survey_data = {"title": "Survey at Inatel", "orgid": 2}
        await client.post("/api/v1/surveys/", json=survey_data, headers=headers)

        response = await client.get("/api/v1/surveys/org/2", headers=headers)
        assert response.status_code == HTTPStatus.OK
        
        response_json = response.json()
        assert isinstance(response_json, list)
        assert any(survey["orgid"] == 2 for survey in response_json)

@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
async def test_api_update_survey(access_token_orgadmin):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {access_token_orgadmin}"}
        survey_data = {"title": "Survey at Inatel", "orgid": 2}
        create_response = await client.post("/api/v1/surveys/", json=survey_data, headers=headers)
        survey_id = create_response.json()["id"]

        update_data = {"title": "Updated Survey", "orgid": 2}
        response = await client.put(f"/api/v1/surveys/{survey_id}", json=update_data, headers=headers)
        assert response.status_code == HTTPStatus.OK
        
        response_json = response.json()
        assert response_json["title"] == "Updated Survey"
        assert response_json["orgid"] == 2

@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
async def test_api_delete_survey(access_token_orgadmin):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        orgid = 2
        survey_data = {
            "title": "Survey at Inatel",
            "orgid": orgid
        }
        headers = {"Authorization": f"Bearer {access_token_orgadmin}"}

        # create a survey
        response = await client.post("/api/v1/surveys/", json=survey_data, headers=headers)
        surveyid = response.json()["id"]

        # delete the survey
        response = await client.delete(f"/api/v1/surveys/{surveyid}", headers=headers)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "message": "Survey deleted successfully"
        }