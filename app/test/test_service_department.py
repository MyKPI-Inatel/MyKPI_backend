import pytest
from unittest.mock import AsyncMock
from service.department import Department
from model.department import DepartmentCreate, DepartmentBase
from dao.department import DepartmentDAO

@pytest.mark.asyncio
@pytest.mark.dept
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
