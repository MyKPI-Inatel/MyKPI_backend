import pytest
from http import HTTPStatus
from httpx import ASGITransport, AsyncClient

from service.department import Department

from main import appServer

# POST /api/v1/departments
@pytest.mark.asyncio
@pytest.mark.dept
@pytest.mark.functional
@pytest.mark.auth
@pytest.mark.employee
async def test_auth_create_department_employee(access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        department_data = {
            "name": "RH",
            "orgid": 2
        }
        
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = await client.post("/api/v1/departments/", json=department_data, headers=headers)

        assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.dept
@pytest.mark.functional
@pytest.mark.auth
async def test_auth_create_department_unauthorized():
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        department_data = {
            "name": "RH",
            "orgid": 2
        }
        
        response = await client.post("/api/v1/departments/", json=department_data)

        assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
@pytest.mark.dept
@pytest.mark.functional
@pytest.mark.auth
@pytest.mark.orgadmin
async def test_auth_create_department_for_wrong_org(access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        department_data = {
            "name": "RH",
            "orgid": 1
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = await client.post("/api/v1/departments/", json=department_data, headers=headers)

        assert response.status_code == HTTPStatus.FORBIDDEN