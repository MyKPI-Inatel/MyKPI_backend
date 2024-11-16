import pytest, pytest_asyncio
from http import HTTPStatus
from httpx import ASGITransport, AsyncClient

from main import appServer

@pytest_asyncio.fixture
async def access_token_superadmin():
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        login_data = {
            "username": "admin@mykpi.online",
            "password": "senha"
        }
        response = await client.post("/api/v1/login", data=login_data)
        return response.json()["access_token"]

@pytest_asyncio.fixture
async def access_token_orgadmin():
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        login_data = {
            "username": "admin@inatel.br",
            "password": "senha"
        }
        response = await client.post("/api/v1/login", data=login_data)
        return response.json()["access_token"]

@pytest.mark.asyncio
@pytest.mark.org
@pytest.mark.functional
async def test_api_create_organization(access_token_superadmin):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        # Sample data for the organization
        organization_data = {
            "name": "Netflix"
        }
        headers = {"Authorization": f"Bearer {access_token_superadmin}"}
        
        # Send a POST request to create a organization
        response = await client.post("/api/v1/organizations/", json=organization_data, headers=headers)

        # Assert the response status code
        assert response.status_code == HTTPStatus.CREATED
        
        # Assert the returned data matches the expected format
        assert response.json() == {
            "id": 4,
            "name": "Netflix",
        }


@pytest.mark.asyncio
@pytest.mark.org
@pytest.mark.functional
async def test_api_get_organization(access_token_orgadmin):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        orgid = 2
        headers = {"Authorization": f"Bearer {access_token_orgadmin}"}

        # Send a GET request to create a organization
        response = await client.get(f"/api/v1/organizations/{orgid}", headers=headers)

        # Assert the response status code
        assert response.status_code == HTTPStatus.OK
        
        # Assert the returned data matches the expected format
        assert response.json() == {
            "id": 2,
            "name": "INATEL"
        }


@pytest.mark.asyncio
@pytest.mark.org
@pytest.mark.functional
async def test_api_get_all_organizations(access_token_superadmin):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        headers = {"Authorization": f"Bearer {access_token_superadmin}"}

        # Send a GET request to create a organization
        response = await client.get("/api/v1/organizations/", headers=headers)

        # Assert the response status code
        assert response.status_code == HTTPStatus.OK
        
        # Assert the returned data matches the expected format
        assert response.json() == [
            {"id": 1, "name": "MY-KPI"},
            {"id": 2, "name": "INATEL"},
            {"id": 3, "name": "4Intelligence"}
        ]


@pytest.mark.asyncio
@pytest.mark.org
@pytest.mark.functional
async def test_api_update_organization(access_token_orgadmin):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        orgid = 2
        organization_data = {
            "name": "Netflix"
        }
        headers = {"Authorization": f"Bearer {access_token_orgadmin}"}

        # Send a PUT request to create a organization
        response = await client.put(f"/api/v1/organizations/{orgid}", json=organization_data, headers=headers)

        # Assert the response status code
        assert response.status_code == HTTPStatus.OK
        
        # Assert the returned data matches the expected format
        assert response.json() == {
            "id": 2,
            "name": "Netflix"
        }


@pytest.mark.asyncio
@pytest.mark.org
@pytest.mark.functional
async def test_api_conflict_deleting_organization(access_token_superadmin):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        orgid = 1
        headers = {"Authorization": f"Bearer {access_token_superadmin}"}

        response = await client.delete(f"/api/v1/organizations/{orgid}", headers=headers)

        assert response.status_code == HTTPStatus.CONFLICT

        assert response.json() == {
            "detail": "Unable to delete organization: related data exists in another table."
        }


@pytest.mark.asyncio
@pytest.mark.org
@pytest.mark.functional
async def test_api_delete_organization(access_token_superadmin):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        orgname = "Netflix"
        headers = {"Authorization": f"Bearer {access_token_superadmin}"}

        # create organization
        response = await client.post("/api/v1/organizations/", json={"name": orgname}, headers=headers)

        orgid = response.json()["id"]

        # Send a DELETE request to create a organization
        response = await client.delete(f"/api/v1/organizations/{orgid}", headers=headers)

        # Assert the response status code
        assert response.status_code == HTTPStatus.OK

        assert response.json() == {
            "message": "Organization deleted successfully"
        }