import os

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from http import HTTPStatus

from jwt import DecodeError, decode, encode, exceptions
from pwdlib import PasswordHash

from model.user import UserBase, UserType
from model.token import TokenData

from service.user import User

SECRET_KEY = os.getenv('SECRET_KEY', '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = PasswordHash.recommended()

def create_access_token(data: dict):
    
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode['exp'] = expire
    return encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/login')


async def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        HTTPStatus.UNAUTHORIZED, 'Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if username := payload.get('sub'):
            token_data = TokenData(username=username)
        else:
            raise credentials_exception
    except DecodeError as e:
        raise credentials_exception from e
    except exceptions.ExpiredSignatureError as e:
        raise HTTPException(
            HTTPStatus.UNAUTHORIZED,
            'Token expired',
            headers={'WWW-Authenticate': 'Bearer'},
        ) from e

    user = await User.get_user_by_email(token_data.username)

    if not user:
        raise credentials_exception

    return user

def verify_permissions(user: UserBase, minimum_usertype: UserType, criteria: dict = None):
    if user.usertype.level < minimum_usertype.level:
        raise HTTPException(HTTPStatus.FORBIDDEN, 'Not enough permissions')
    
    if criteria and user.usertype.level != UserType.superadmin.level:
        for key, value in criteria.items():
            if getattr(user, key) != value:
                raise HTTPException(HTTPStatus.FORBIDDEN, 'Not enough permissions')