from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from internal.security import create_access_token, get_current_user, get_password_hash, verify_password, verify_permissions

from model.user import UserType, CurrentUser, EmployeeBase, UserBase, UserCreate, UserUpdate, EmployeeCreate
from model.token import Token
from model.user import UserType

from service.user import User
from service.department import Department

router = APIRouter()

@router.post('/register',
    status_code=HTTPStatus.CREATED,
    response_model=UserBase,
    summary="Create a new user",
    description="This endpoint allows you to register yourself as an employee."
    )
async def create_user(user: UserCreate):
    exists = await User.exists(user.email)

    if exists:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Email already exists')

    user = UserBase(**user.model_dump(), usertype='employee')

    hashed_password = get_password_hash(user.password)

    user.password = hashed_password

    return await User.create_user(user)

@router.post('/employee', 
    status_code=HTTPStatus.CREATED, 
    response_model=UserBase,
    summary="Create a new employee, you must be an organization admin",
    description="This endpoint allows you to create a new employee, you must be an organization admin. You can only create employees for your organization."
)
async def create_user(user: EmployeeCreate, 
                      current_user: CurrentUser = Depends(get_current_user)):

    exists = await User.exists(user.email)

    if exists:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Email already exists')

    user = UserBase(**user.model_dump(), usertype='employee', orgid=current_user.orgid, password="Changeme_123")

    verify_permissions(current_user, UserType.orgadmin, {'orgid': user.orgid})

    hashed_password = get_password_hash(user.password)

    user.password = hashed_password

    #verify if department belongs to the organization
    try:
        await Department.get_department(user.deptid, user.orgid)
    except HTTPException as e:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            'Department does not belong to the organization',
        ) from e

    return await User.create_user(user)

@router.put('/users/{user_id}/', 
    status_code=HTTPStatus.OK,
    response_model=UserBase,
    summary="Update a user",
    description="Update the details of a specific user by its ID."
)
def update_user(
    user_id: int,
    user: UserUpdate,
    current_user: CurrentUser = Depends(get_current_user)
):
    verify_permissions(current_user, UserType.employee, {'id': user_id})
    try:
        current_user.name = user.name
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email

        return User.update_user(current_user)
    except HTTPException as e:
        raise HTTPException(HTTPStatus.CONFLICT, 'Email already exists') from e


@router.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    summary="Delete a user",
    description="Delete a specific user by its ID."
)
async def delete_user(
    user_id: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    verify_permissions(current_user, UserType.orgadmin, {'orgid': current_user.orgid})
    try:
        await User.delete_user(user_id, current_user.orgid)
    except HTTPException as e:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'User not found') from e

    return {'message': 'User deleted successfully'}


@router.post('/login',
    status_code=HTTPStatus.OK,
    response_model=Token,
    summary="Login for access token",
    description="Login for access token"
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await User.get_user_by_email(form_data.username)

    if not user:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Incorrect email or password')

    if not verify_password(form_data.password, user.password):
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Incorrect email or password')

    token_data = {k: v for k, v in user.model_dump().items() if k != 'password'}
    token_data['sub'] = user.email

    access_token = create_access_token(data=token_data)

    return {'access_token': access_token, 'token_type': 'bearer'}

# get users by orgid
@router.get('/users',
    status_code=HTTPStatus.OK,
    response_model=list[EmployeeBase],
    summary="Get all users by organization ID",
    description="Retrieve a list of all users associated with a specific organization ID."
)
async def get_users_by_orgid(
    current_user: CurrentUser = Depends(get_current_user)
):
    verify_permissions(current_user, UserType.orgadmin, {'orgid': current_user.orgid})

    return await User.get_users_by_orgid(current_user.orgid)