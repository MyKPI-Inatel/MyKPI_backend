import pytest, pytest_asyncio
from http import HTTPStatus
from httpx import ASGITransport, AsyncClient

from dao.database import Database
from service.department import Department

from main import appServer

@pytest_asyncio.fixture()
async def reset_database():
    await Database.reset_database()

@pytest_asyncio.fixture
async def access_token():
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        login_data = {
            "username": "admin@inatel.br",
            "password": "senha"
        }
        response = await client.post("/api/v1/login", data=login_data)
        return response.json()["access_token"]

@pytest.mark.asyncio
@pytest.mark.dept
@pytest.mark.functional
async def test_api_create_department(reset_database, access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        last_id = await Department.get_last_id()

        orgid = 2

        # Sample data for the department
        department_data = {
            "name": "RH",
            "orgid": orgid
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Send a POST request to create a department
        response = await client.post("/api/v1/departments/", json=department_data, headers=headers)

        # Assert the response status code
        assert response.status_code == HTTPStatus.CREATED
        
        # Assert the returned data matches the expected format
        assert response.json() == {
            "id": last_id+1,
            "name": "RH",
            "orgid": orgid
        }

@pytest.mark.asyncio
@pytest.mark.dept
@pytest.mark.functional
async def test_api_get_department(reset_database, access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        headers = {"Authorization": f"Bearer {access_token}"}

        # Send a GET request to create a department
        response = await client.get("/api/v1/departments/org/2/2", headers=headers)

        # Assert the response status code
        assert response.status_code == HTTPStatus.OK
        
        # Assert the returned data matches the expected format
        assert response.json() == {
            "id": 2,
            "name": "Recursos Humanos",
            "orgid": 2
        }


@pytest.mark.asyncio
@pytest.mark.dept
@pytest.mark.functional
async def test_api_get_departments_by_org(reset_database, access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        orgid = 2
        headers = {"Authorization": f"Bearer {access_token}"}

        # Send a GET request to create a department
        response = await client.get(f"/api/v1/departments/org/{orgid}", headers=headers)

        # Assert the response status code
        assert response.status_code == HTTPStatus.OK
        
        # Assert the returned data matches the expected format
        assert response.json() == [
            {"id": 2, "name": "Recursos Humanos", "orgid": orgid},
            {"id": 3, "name": "Desenvolvimento", "orgid": orgid},
            {"id": 4, "name": "Engenharia", "orgid": orgid}
        ]


@pytest.mark.asyncio
@pytest.mark.dept
@pytest.mark.functional
async def test_api_update_department(reset_database, access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        departmentid = 2
        department_data = {
            "name": "TI"
        }
        headers = {"Authorization": f"Bearer {access_token}"}

        orgid = 2
        response = await client.put(f"/api/v1/departments/org/{orgid}/{departmentid}", json=department_data, headers=headers)

        assert response.status_code == HTTPStatus.OK
        
        assert response.json() == {
            "id": departmentid,
            "name": "TI",
            "orgid": orgid
        }

@pytest.mark.asyncio
@pytest.mark.dept
@pytest.mark.functional
async def test_api_conflict_deleting_department(reset_database, access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        departmentid = 2
        orgid = 2
        headers = {"Authorization": f"Bearer {access_token}"}

        response = await client.delete(f"/api/v1/departments/org/{orgid}/{departmentid}", headers=headers)

        assert response.status_code == HTTPStatus.CONFLICT

        assert response.json() == {
            "detail": "Unable to delete department: related data exists in another table."
        }

@pytest.mark.asyncio
@pytest.mark.dept
@pytest.mark.functional
async def test_api_delete_department(reset_database, access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        orgid = 2
        department_data = {
            "name": "RH",
            "orgid": orgid
        }
        headers = {"Authorization": f"Bearer {access_token}"}

        # create a department
        response = await client.post("/api/v1/departments/", json=department_data, headers=headers)
        departmentid = response.json()["id"]

        # delete the department
        response = await client.delete(f"/api/v1/departments/org/{orgid}/{departmentid}", headers=headers)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "message": "Department deleted successfully"
        }