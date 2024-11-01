from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from model.user import UserBase, UserCreate, UserUpdate
from model.token import Token
from service.user import User
from internal.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

router = APIRouter()

@router.post('/register', status_code=HTTPStatus.CREATED, response_model=UserBase)
async def create_user(user: UserCreate):
    exists = await User.exists(user.email)

    if exists:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email already exists',
        )
    
    user = UserBase(**user.model_dump(), usertype='employee')

    hashed_password = get_password_hash(user.password)

    user.password = hashed_password

    user_data = await User.create_user(user)

    return user_data


@router.put('/users/{user_id}', response_model=UserBase)
def update_user(
    user_id: int,
    user: UserUpdate,
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    try:
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email

        user_data = User.update_user(current_user)

        return user_data

    except HTTPException:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@router.delete('/users/{user_id}')
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    result = await User.delete_user(user_id)

    return {'message': 'User deleted'}


@router.post('/login', response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await User.get_user_by_email(form_data.username)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    token_data = {k: v for k, v in user.model_dump().items() if k != 'password'}
    token_data['sub'] = user.email

    access_token = create_access_token(data=token_data)

    return {'access_token': access_token, 'token_type': 'bearer'}