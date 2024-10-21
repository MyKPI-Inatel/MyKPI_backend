import pytest
from httpx import ASGITransport, AsyncClient
from main import appServer

# TODO: Make a fixture for resetting the database before each test

@pytest.mark.asyncio
@pytest.mark.dept
@pytest.mark.functional
async def test_create_department():
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
            "id": 13,
            "name": "RH",
            "orgid": 1
        }