from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from dao.database import Database
from router.organization import router as organization
from router.question import router as question
from router.department import router as department
from router.survey import router as survey
from router.user import router as user

appServer = FastAPI()

appServer.include_router(question, prefix="/api/v1/questions", tags=["Questions"])
appServer.include_router(department, prefix="/api/v1/departments", tags=["Departments"])
appServer.include_router(organization, prefix="/api/v1/organizations", tags=["Organizations"])
appServer.include_router(survey, prefix="/api/v1/surveys", tags=["Surveys"])
appServer.include_router(user, prefix="/api/v1", tags=["Users"])

# Adicione o middleware CORS
appServer.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota para resetar o banco de dados
@appServer.post("/api/v1/db-reset/")
async def reset_database():
    await Database.reset_database()
    return {"message": "Database reset successfully"}

# Função para healthcheck
@appServer.get("/")
async def healthcheck():
    return {"status": "ok"}
