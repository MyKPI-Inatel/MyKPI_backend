import pytest
from unittest.mock import AsyncMock
from service.organization import Organization
from model.organization import OrganizationCreate, OrganizationBase
from dao.organization import OrganizationDAO

@pytest.mark.asyncio
@pytest.mark.org
async def test_create_organization(mocker):
    # Mock input and expected return values
    organization_data = OrganizationCreate(name="HR")
    expected_return = OrganizationBase(id=1, name="HR")

    # Mock the insert method of the DAO
    mocker.patch.object(OrganizationDAO, 'insert', new_callable=AsyncMock, return_value=expected_return)

    # Call the function we're testing
    result = await Organization.create_organization(organization_data)

    # Asserts that the DAO's insert method was called with the correct input
    OrganizationDAO.insert.assert_called_once_with(organization_data)

    # Asserts that the result is as expected
    assert result == expected_return