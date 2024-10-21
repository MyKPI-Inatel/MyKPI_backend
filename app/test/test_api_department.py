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
async def test_create_department(reset_database):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        # Sample data for the department
        department_data = {
            "name": "RH",
            "orgid": 1
        }
        
        # Send a POST request to create a department
        response = await client.post("/api/v1/departments/", json=department_data)

        # Assert the response status code
        assert response.status_code == 200
        
        # Assert the returned data matches the expected format
        assert response.json() == {
            "id": 8,
            "name": "RH",
            "orgid": 1
        }

@pytest.mark.asyncio
@pytest.mark.dept
@pytest.mark.functional
async def test_get_department(reset_database):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        # Send a GET request to create a department
        response = await client.get("/api/v1/departments/org/1/1")

        # Assert the response status code
        assert response.status_code == 200
        
        # Assert the returned data matches the expected format
        assert response.json() == {
            "id": 1,
            "name": "Geral",
            "orgid": 1
        }