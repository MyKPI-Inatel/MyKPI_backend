import pytest
from httpx import ASGITransport, AsyncClient
from app.dao.database import Database
from main import appServer
import pytest_asyncio

@pytest_asyncio.fixture()
async def reset_database():
    await Database.reset_database()

@pytest.mark.asyncio
@pytest.mark.org
@pytest.mark.functional
async def test_api_create_organization(reset_database):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        # Sample data for the organization
        organization_data = {
            "name": "Netflix"
        }
        
        # Send a POST request to create a organization
        response = await client.post("/api/v1/organizations/", json=organization_data)

        # Assert the response status code
        assert response.status_code == 200
        
        # Assert the returned data matches the expected format
        assert response.json() == {
            "id": 4,
            "name": "Netflix",
        }


@pytest.mark.asyncio
@pytest.mark.org
@pytest.mark.functional
async def test_api_get_organization(reset_database):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        orgid = 1

        # Send a GET request to create a organization
        response = await client.get(f"/api/v1/organizations/{orgid}")

        # Assert the response status code
        assert response.status_code == 200
        
        # Assert the returned data matches the expected format
        assert response.json() == {
            "id": 1,
            "name": "MY-KPI"
        }


@pytest.mark.asyncio
@pytest.mark.org
@pytest.mark.functional
async def test_api_get_all_organizations(reset_database):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        # Send a GET request to create a organization
        response = await client.get("/api/v1/organizations/")

        # Assert the response status code
        assert response.status_code == 200
        
        # Assert the returned data matches the expected format
        assert response.json() == [
            {"id": 1, "name": "MY-KPI"},
            {"id": 2, "name": "INATEL"},
            {"id": 3, "name": "4Intelligence"}
        ]


@pytest.mark.asyncio
@pytest.mark.org
@pytest.mark.functional
async def test_api_update_organization(reset_database):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        orgid = 1
        organization_data = {
            "name": "Netflix"
        }

        # Send a PUT request to create a organization
        response = await client.put(f"/api/v1/organizations/{orgid}", json=organization_data)

        # Assert the response status code
        assert response.status_code == 200
        
        # Assert the returned data matches the expected format
        assert response.json() == {
            "id": 1,
            "name": "Netflix"
        }


@pytest.mark.asyncio
@pytest.mark.org
@pytest.mark.functional
async def test_api_conflict_deleting_organization(reset_database):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        orgid = 1
        response = await client.delete(f"/api/v1/organizations/{orgid}")

        assert response.status_code == 409

        assert response.json() == {
            "detail": "Unable to delete organization: related data exists in another table."
        }


@pytest.mark.asyncio
@pytest.mark.org
@pytest.mark.functional
async def test_api_delete_organization(reset_database):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        orgname = "Netflix"

        # create organization
        response = await client.post("/api/v1/organizations/", json={"name": orgname})

        orgid = response.json()["id"]

        # Send a DELETE request to create a organization
        response = await client.delete(f"/api/v1/organizations/{orgid}")

        # Assert the response status code
        assert response.status_code == 200

        assert response.json() == {
            "message": "Organization deleted successfully"
        }