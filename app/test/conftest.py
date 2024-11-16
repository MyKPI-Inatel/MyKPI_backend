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
async def get_access_token(email, password):
    async with AsyncClient(transport=ASGITransport(app=appServer), base_url="http://test") as client:
        login_data = {"username": email, "password": password}
        response = await client.post("/api/v1/login", data=login_data)
        return response.json()["access_token"]

# Fixture para o token de acesso baseado no marcador
@pytest_asyncio.fixture
async def access_token(request):
    # Checar os marcadores e configurar o email e a senha de acordo
    if "superadmin" in request.node.keywords:
        email, password = "admin@mykpi.online", "senha"
    elif "orgadmin" in request.node.keywords:
        email, password = "admin@inatel.br", "senha"
    elif "employee" in request.node.keywords:
        email, password = "dev@inatel.br", "senha"
    else:
        raise ValueError("Invalid marker")

    return await get_access_token(email, password)

# Registrar a fixture reset_database como um hook para todos os testes funcionais
@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    for item in items:
        if "functional" in item.keywords:
            item.fixturenames.append("reset_database")
