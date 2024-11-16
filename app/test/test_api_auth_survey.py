from http import HTTPStatus
import pytest
from httpx import ASGITransport, AsyncClient

from main import appServer

@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
@pytest.mark.auth
@pytest.mark.orgadmin
async def test_api_auth_get_surveys_orgadmin(access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.get("/api/v1/surveys/", headers=headers)
        assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
@pytest.mark.auth
@pytest.mark.employee
async def test_api_auth_get_surveys_employee(access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.get("/api/v1/surveys/", headers=headers)
        assert response.status_code == HTTPStatus.FORBIDDEN
