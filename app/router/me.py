from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException

from internal.security import get_current_user, get_password_hash, verify_permissions

from model.user import UserType, CurrentUser, UserBase, UserUpdate
from model.user import UserType

from service.user import User

router = APIRouter()

@router.put('/', response_model=UserBase)
async def update_me(
    user: UserUpdate,
    current_user: CurrentUser = Depends(get_current_user)
):
    verify_permissions(current_user, UserType.employee)
    try:
        current_user.name = user.name
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email

        return User.self_update_user(current_user)
    except HTTPException as e:
        raise HTTPException(HTTPStatus.CONFLICT, 'Email already exists') from e
    
@router.get('/',
            response_model=UserBase,
            summary="Get current user",
            description="Get the current user's details."
            )
async def get_me(
    current_user: CurrentUser = Depends(get_current_user)
):
    return current_user