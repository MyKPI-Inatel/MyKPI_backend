from http import HTTPStatus
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from dao.database import Database
from main import appServer

# Fixture para resetar o banco de dados
@pytest_asyncio.fixture()
async def reset_database():
    await Database.reset_database()

# Função auxiliar para obter o token de acesso
async def get_access_token(username, password):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        login_data = {"username": username, "password": password}
        response = await client.post("/api/v1/login", data=login_data)
        return response.json()["access_token"]

# Fixture para o token de acesso de orgadmin
@pytest_asyncio.fixture
async def access_token_orgadmin():
    return await get_access_token("admin@inatel.br", "senha")

# Fixture para o token de acesso de employee
@pytest_asyncio.fixture
async def access_token_employee():
    return await get_access_token("dev@inatel.br", "senha")

# Teste funcional para verificar acesso às pesquisas com orgadmin
@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
@pytest.mark.auth
async def test_api_get_surveys_orgadmin(reset_database, access_token_orgadmin):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {access_token_orgadmin}"}
        response = await client.get("/api/v1/surveys/", headers=headers)
        assert response.status_code == HTTPStatus.FORBIDDEN

# Teste funcional para verificar acesso às pesquisas com employee
@pytest.mark.asyncio
@pytest.mark.survey
@pytest.mark.functional
@pytest.mark.auth
async def test_api_get_surveys_employee(reset_database, access_token_employee):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        headers = {"Authorization": f"Bearer {access_token_employee}"}
        response = await client.get("/api/v1/surveys/", headers=headers)
        assert response.status_code == HTTPStatus.FORBIDDEN
