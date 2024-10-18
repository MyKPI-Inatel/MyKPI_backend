# router/user.py
from fastapi import APIRouter, HTTPException
from model.user import UserBase, UserLogin
from dao.user import UserDAO
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os
from typing import Optional

router = APIRouter()

# Usaremos este exemplo apenas para fins de demonstração.
# Em um ambiente de produção, você deve armazenar as senhas de forma segura,
# como usando hash e salt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configurações do JWT
SECRET_KEY = os.environ.get("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = "HS256"

# Função para gerar o token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para registrar um usuário
@router.post("/register/")
async def register_user(user: UserBase):

    result = await UserDAO.insert(user)
    
    if result is not None:
        try:
            user = await UserDAO.get_by_email(user.email)

            print(user)
            
            user.password = None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")
        return {"message": "User registered successfully", "user": user}

# Função para autenticar um usuário
@router.post("/login/")
async def login_user(user: UserLogin):
    try:
        password = await UserDAO.get_password(user.email)

        if password is None:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        stored_password = password

        if not pwd_context.verify(user.password, stored_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

    try:
        user = await UserDAO.get_by_email(user.email)
        
        access_token = create_access_token(data=user.toJSON())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")

    return {"access_token": access_token, "token_type": "bearer", "user": user}
