import pytest
from unittest.mock import AsyncMock

from dao.organization import OrganizationDAO

from model.organization import OrganizationCreate, OrganizationBase, OrganizationUpdate

from service.organization import Organization

@pytest.mark.asyncio
@pytest.mark.org
@pytest.mark.unit
async def test_svc_create_organization(mocker):
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
@pytest.mark.unit
async def test_svc_get_organization(mocker):
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
@pytest.mark.unit
async def test_svc_get_all_organizations(mocker):
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


@pytest.mark.asyncio
@pytest.mark.org
@pytest.mark.unit
async def test_svc_update_organization(mocker):
    # Mock input and expected return values
    organizationid = 1
    organization_data = OrganizationUpdate(name="Instituto Nacional de Telecomunicacoes")
    expected_return = OrganizationBase(id=1, name="Instituto Nacional de Telecomunicacoes")

    # Mock the update method of the DAO
    mocker.patch.object(OrganizationDAO, 'update', new_callable=AsyncMock, return_value=expected_return)

    # Call the function we're testing
    result = await Organization.update_organization(organizationid, organization_data)

    # Asserts that the DAO's update method was called with the correct inputs
    OrganizationDAO.update.assert_called_once_with(organizationid, organization_data)

    # Asserts that the result is as expected
    assert result == expected_return


@pytest.mark.asyncio
@pytest.mark.org
@pytest.mark.unit
async def test_svc_delete_organization(mocker):
    # Mock input and expected return values
    organizationid = 1
    expected_return = True

    # Mock the delete method of the DAO
    mocker.patch.object(OrganizationDAO, 'delete', new_callable=AsyncMock, return_value=expected_return)

    # Call the function we're testing
    result = await Organization.delete_organization(organizationid)

    # Asserts that the DAO's delete method was called with the correct input
    OrganizationDAO.delete.assert_called_once_with(organizationid)

    # Asserts that the result is as expected
    assert result == expected_return