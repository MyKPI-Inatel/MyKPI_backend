import pytest
from http import HTTPStatus
from httpx import ASGITransport, AsyncClient

from main import appServer

@pytest.mark.asyncio
@pytest.mark.org
@pytest.mark.functional
@pytest.mark.superadmin
async def test_api_create_organization(access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        # Sample data for the organization
        organization_data = {
            "name": "Netflix"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Send a POST request to create an organization
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
@pytest.mark.orgadmin
async def test_api_get_organization(access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        orgid = 2
        headers = {"Authorization": f"Bearer {access_token}"}

        response = await client.get(f"/api/v1/organizations/{orgid}", headers=headers)

        assert response.status_code == HTTPStatus.OK
        
        assert response.json() == {
            "id": 2,
            "name": "INATEL"
        }


@pytest.mark.asyncio
@pytest.mark.org
@pytest.mark.functional
@pytest.mark.superadmin
async def test_api_get_all_organizations(access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        headers = {"Authorization": f"Bearer {access_token}"}

        response = await client.get("/api/v1/organizations/", headers=headers)

        assert response.status_code == HTTPStatus.OK
        
        assert response.json() == [
            {"id": 1, "name": "MY-KPI"},
            {"id": 2, "name": "INATEL"},
            {"id": 3, "name": "4Intelligence"}
        ]


@pytest.mark.asyncio
@pytest.mark.org
@pytest.mark.functional
@pytest.mark.orgadmin
async def test_api_update_organization(access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        orgid = 2
        organization_data = {
            "name": "Netflix"
        }
        headers = {"Authorization": f"Bearer {access_token}"}

        response = await client.put(f"/api/v1/organizations/{orgid}", json=organization_data, headers=headers)

        assert response.status_code == HTTPStatus.OK
        
        assert response.json() == {
            "id": 2,
            "name": "Netflix"
        }


@pytest.mark.asyncio
@pytest.mark.org
@pytest.mark.functional
@pytest.mark.superadmin
async def test_api_conflict_deleting_organization(access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        orgid = 1
        headers = {"Authorization": f"Bearer {access_token}"}

        response = await client.delete(f"/api/v1/organizations/{orgid}", headers=headers)

        assert response.status_code == HTTPStatus.CONFLICT

        assert response.json() == {
            "detail": "Unable to delete organization: related data exists in another table."
        }


@pytest.mark.asyncio
@pytest.mark.org
@pytest.mark.functional
@pytest.mark.superadmin
async def test_api_delete_organization(access_token):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:

        orgname = "Netflix"
        headers = {"Authorization": f"Bearer {access_token}"}

        # Send a POST request to create an organization
        response = await client.post("/api/v1/organizations/", json={"name": orgname}, headers=headers)

        orgid = response.json()["id"]

        # Send a DELETE request
        response = await client.delete(f"/api/v1/organizations/{orgid}", headers=headers)

        # Assert the response status code
        assert response.status_code == HTTPStatus.OK

        assert response.json() == {
            "message": "Organization deleted successfully"
        }