from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from passlib.context import CryptContext
from typing import Optional, List
from jose import jwt
from datetime import datetime, timedelta
import os

from model.user import UserBase, UserLogin
from dao.user import UserDAO
from dao.database import Database

from model.survey import SurveyBase, SurveyCreate, SurveyUpdate
from dao.survey import SurveyDAO

from model.organization import OrganizationBase, OrganizationCreate, OrganizationUpdate
from dao.organization import OrganizationDAO

appServer = FastAPI()

# Adicione o middleware CORS
appServer.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Usaremos este exemplo apenas para fins de demonstração.
# Em um ambiente de produção, você deve armazenar as senhas de forma segura,
# como usando hash e salt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configurações do banco de dados
DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/mykpi")
# Configurações do JWT
SECRET_KEY = os.environ.get("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Função para verificar a senha
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Função para gerar o token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Rota para resetar o banco de dados
@appServer.post("/api/v1/db-reset/")
async def reset_database():
    await Database.reset_database()
    return {"message": "Database reset successfully"}

# Função para registrar um usuário
@appServer.post("/api/v1/register/")
async def register_user(user: UserBase):
    result = await UserDAO.insert(user)
    
    if result is not None:
        try:
            user = await UserDAO.get(email=user.email)
            user = user[0]
            # Remove password from response
            user = {key: value for key, value in user.items() if key != "password"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")
        return {"message": "User registered successfully", "user": user}

# Função para autenticar um usuário
@appServer.post("/api/v1/login/")
async def login_user(user: UserLogin):
    try:
        record = await UserDAO.get_password(user.email)

        if record is None:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        stored_password = record

        if not pwd_context.verify(user.password, stored_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        access_token = create_access_token(data={"sub": user.email})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")
    
    # Pick username, usertype and id
    try:
        user = await UserDAO.get(email=user.email)
        user = user[0]
        # Remove password from response
        user = {key: value for key, value in user.items() if key != "password"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")

    return {"access_token": access_token, "token_type": "bearer", "user": user}

# Função para healthcheck
@appServer.get("/")
async def healthcheck():
    return {"status": "ok"}

# Endpoint para listar todos os usuários
@appServer.get("/api/v1/users/", response_model=List[UserBase])
async def get_users():
    try:
        users = await UserDAO.get_all()
        # Remove senhas dos usuários na resposta
        users = [{key: value for key, value in user.items() if key != "password"} for user in users]
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

# Endpoints para Survey
@appServer.post("/api/v1/surveys/", response_model=SurveyBase)
async def create_survey(survey: SurveyCreate):
    result = await SurveyDAO.insert(survey)
    if result is None:
        raise HTTPException(status_code=400, detail="Error creating survey")
    return result

@appServer.get("/api/v1/surveys/", response_model=List[SurveyBase])
async def get_surveys():
    surveys = await SurveyDAO.get_all()
    return surveys

@appServer.get("/api/v1/surveys/{survey_id}", response_model=SurveyBase)
async def get_survey(survey_id: int):
    survey = await SurveyDAO.get(survey_id)
    if survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey

@appServer.put("/api/v1/surveys/{survey_id}", response_model=SurveyBase)
async def update_survey(survey_id: int, survey: SurveyUpdate):
    result = await SurveyDAO.update(survey_id, survey)
    if result is None:
        raise HTTPException(status_code=400, detail="Error updating survey")
    return result

@appServer.delete("/api/v1/surveys/{survey_id}")
async def delete_survey(survey_id: int):
    result = await SurveyDAO.delete(survey_id)
    if not result:
        raise HTTPException(status_code=404, detail="Survey not found")
    return {"message": "Survey deleted successfully"}

# Endpoints para Organization
@appServer.post("/api/v1/organizations/", response_model=OrganizationBase)
async def create_organization(organization: OrganizationCreate):
    result = await OrganizationDAO.insert(organization)
    if result is None:
        raise HTTPException(status_code=400, detail="Error creating organization")
    return result

@appServer.get("/api/v1/organizations/", response_model=List[OrganizationBase])
async def get_organizations():
    organizations = await OrganizationDAO.get_all()
    return organizations

@appServer.get("/api/v1/organizations/{org_id}", response_model=OrganizationBase)
async def get_organization(org_id: int):
    organization = await OrganizationDAO.get(org_id)
    if organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@appServer.put("/api/v1/organizations/{org_id}", response_model=OrganizationBase)
async def update_organization(org_id: int, organization: OrganizationUpdate):
    result = await OrganizationDAO.update(org_id, organization)
    if result is None:
        raise HTTPException(status_code=400, detail="Error updating organization")
    return result

@appServer.delete("/api/v1/organizations/{org_id}")
async def delete_organization(org_id: int):
    result = await OrganizationDAO.delete(org_id)
    if not result:
        raise HTTPException(status_code=404, detail="Organization not found")
    return {"message": "Organization deleted successfully"}
