import pytest
from httpx import ASGITransport, AsyncClient
from app.dao.database import Database
from main import appServer
import pytest_asyncio

@pytest_asyncio.fixture()
async def reset_database():
    await Database.reset_database()

@pytest.mark.asyncio
@pytest.mark.dept
@pytest.mark.functional
async def test_create_organization(reset_database):
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
