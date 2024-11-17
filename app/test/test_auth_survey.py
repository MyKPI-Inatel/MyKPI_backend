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
@pytest.mark.orgadmin
async def test_auth_get_surveys_orgadmin(access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.get("/api/v1/surveys/", headers=headers)
        assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
@pytest.mark.employee
async def test_auth_get_survey_employee(access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {access_token}"}

        response = await client.get("/api/v1/surveys/1", headers=headers)
        assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
@pytest.mark.orgadmin
async def test_api_get_surveys_by_org(access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {access_token}"}

        response = await client.get("/api/v1/surveys/org/2", headers=headers)
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
