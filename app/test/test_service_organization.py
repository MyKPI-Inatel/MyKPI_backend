import pytest
from unittest.mock import AsyncMock
from service.organization import Organization
from model.organization import OrganizationCreate, OrganizationBase
from dao.organization import OrganizationDAO

@pytest.mark.asyncio
@pytest.mark.org
async def test_create_organization(mocker):
    # Mock input and expected return values
    organization_data = OrganizationCreate(name="Inatel")
    expected_return = OrganizationBase(id=1, name="Inatel")

    # Mock the insert method of the DAO
    mocker.patch.object(OrganizationDAO, 'insert', new_callable=AsyncMock, return_value=expected_return)

    # Call the function we're testing
    result = await Organization.create_organization(organization_data)

    # Asserts that the DAO's insert method was called with the correct input
    OrganizationDAO.insert.assert_called_once_with(organization_data)

    # Asserts that the result is as expected
    assert result == expected_return

@pytest.mark.asyncio
@pytest.mark.org
async def test_get_organization(mocker):
    # Mock input and expected return values
    organizationid = 1
    expected_return = OrganizationBase(id=1, name="Inatel")

    # Mock the get method of the DAO
    mocker.patch.object(OrganizationDAO, 'get', new_callable=AsyncMock, return_value=expected_return)

    # Call the function we're testing
    result = await Organization.get_organization(organizationid)

    # Asserts that the DAO's get method was called with the correct input
    OrganizationDAO.get.assert_called_once_with(organizationid)

    # Asserts that the result is as expected
    assert result == expected_return

@pytest.mark.asyncio
@pytest.mark.org
async def test_get_all_organizations(mocker):
    # Mock expected return values
    expected_return = [OrganizationBase(id=1, name="INATEL"), OrganizationBase(id=2, name="MyKPI")]

    # Mock the get_all method of the DAO
    mocker.patch.object(OrganizationDAO, 'get_all', new_callable=AsyncMock, return_value=expected_return)

    # Call the function we're testing
    result = await Organization.get_all_organizations()

    # Asserts that the DAO's get_all method was called
    OrganizationDAO.get_all.assert_called_once()

    # Asserts that the result is as expected
    assert result == expected_return
