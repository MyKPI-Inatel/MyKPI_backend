from http import HTTPStatus
import pytest
from httpx import ASGITransport, AsyncClient

from main import appServer

@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
@pytest.mark.auth
@pytest.mark.employee
async def test_auth_create_survey_employee(access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        survey_data = {"title": "Survey at Inatel", "orgid": 2}
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = await client.post("/api/v1/surveys/", json=survey_data, headers=headers)
        assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
@pytest.mark.auth
async def test_auth_create_survey_unauthenticated():
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        survey_data = {"title": "Survey at Inatel", "orgid": 2}
        
        response = await client.post("/api/v1/surveys/", json=survey_data)
        assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
@pytest.mark.auth
@pytest.mark.orgadmin
async def test_auth_get_surveys_orgadmin(access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.get("/api/v1/surveys/", headers=headers)
        assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
@pytest.mark.auth
@pytest.mark.employee
async def test_auth_get_survey_employee(access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {access_token}"}

        response = await client.get("/api/v1/surveys/1", headers=headers)
        assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
@pytest.mark.auth
async def test_auth_get_survey_unauthenticated():
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        response = await client.get("/api/v1/surveys/1")
        assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
@pytest.mark.auth
@pytest.mark.employee
async def test_auth_get_surveys_by_wrong_org(access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {access_token}"}

        response = await client.get("/api/v1/surveys/org/3", headers=headers)
        assert response.status_code == HTTPStatus.FORBIDDEN
        

@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
@pytest.mark.auth
@pytest.mark.employee
async def test_api_update_survey_employee(access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {access_token}"}
        update_data = {"title": "Updated Survey", "orgid": 2}
        response = await client.put("/api/v1/surveys/2", json=update_data, headers=headers)
        assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
@pytest.mark.auth
@pytest.mark.employee
async def test_auth_get_surveys_employee(access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.get("/api/v1/surveys/", headers=headers)
        assert response.status_code == HTTPStatus.FORBIDDEN
