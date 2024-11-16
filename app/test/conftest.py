import pytest, pytest_asyncio
from dao.database import Database

@pytest_asyncio.fixture()
async def reset_database():
    await Database.reset_database()

# Register the reset_database fixture as a pytest hook for all functional tests
@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    for item in items:
        if "functional" in item.keywords:
            item.fixturenames.append("reset_database")
