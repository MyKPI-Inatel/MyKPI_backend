import pytest
from unittest.mock import AsyncMock
from service.department import Department
from model.department import DepartmentCreate, DepartmentBase, DepartmentUpdate
from dao.department import DepartmentDAO

@pytest.mark.asyncio
@pytest.mark.dept
@pytest.mark.unit
async def test_create_department(mocker):
    # Mock input and expected return values
    department_data = DepartmentCreate(name="HR", orgid=2)
    expected_return = DepartmentBase(id=1, name="HR", orgid=2)

    # Mock the insert method of the DAO
    mocker.patch.object(DepartmentDAO, 'insert', new_callable=AsyncMock, return_value=expected_return)

    # Call the function we're testing
    result = await Department.create_department(department_data)

    # Asserts that the DAO's insert method was called with the correct input
    DepartmentDAO.insert.assert_called_once_with(department_data)

    # Asserts that the result is as expected
    assert result == expected_return


@pytest.mark.asyncio
@pytest.mark.dept
@pytest.mark.unit
async def test_get_department(mocker):
    # Mock input and expected return values
    departmentid = 1
    orgid = 2
    expected_return = DepartmentBase(id=1, name="HR", orgid=2)

    # Mock the get method of the DAO
    mocker.patch.object(DepartmentDAO, 'get', new_callable=AsyncMock, return_value=expected_return)

    # Call the function we're testing
    result = await Department.get_department(departmentid, orgid)

    # Asserts that the DAO's get method was called with the correct input
    DepartmentDAO.get.assert_called_once_with(departmentid, orgid)

    # Asserts that the result is as expected
    assert result == expected_return


@pytest.mark.asyncio
@pytest.mark.dept
@pytest.mark.unit
async def test_update_department(mocker):
    # Mock input and expected return values
    departmentid = 1
    department_data = DepartmentUpdate(name="HR")
    orgid = 2
    expected_return = DepartmentBase(id=1, name="HR", orgid=2)

    # Mock the update method of the DAO
    mocker.patch.object(DepartmentDAO, 'update', new_callable=AsyncMock, return_value=expected_return)

    # Call the function we're testing
    result = await Department.update_department(departmentid, department_data, orgid)

    # Asserts that the DAO's update method was called with the correct input
    DepartmentDAO.update.assert_called_once_with(departmentid, department_data, orgid)

    # Asserts that the result is as expected
    assert result == expected_return

@pytest.mark.asyncio
@pytest.mark.dept
@pytest.mark.unit
async def test_delete_department(mocker):
    # Mock input and expected return values
    orgid = 2
    departmentid = 1
    expected_return = True

    # Mock the delete method of the DAO
    mocker.patch.object(DepartmentDAO, 'delete', new_callable=AsyncMock, return_value=expected_return)

    # Call the function we're testing
    result = await Department.delete_department(orgid, departmentid)

    # Asserts that the DAO's delete method was called with the correct input
    DepartmentDAO.delete.assert_called_once_with(orgid, departmentid)

    # Asserts that the result is as expected
    assert result == expected_return