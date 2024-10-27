from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dao.database import Database

from router import organization, question, department, survey, user

appServer = FastAPI()

appServer.include_router(question.router, prefix="/api/v1/questions", tags=["Questions"])
appServer.include_router(department.router, prefix="/api/v1/departments", tags=["Departments"])
appServer.include_router(organization.router, prefix="/api/v1/organizations", tags=["Organizations"])
appServer.include_router(survey.router, prefix="/api/v1/surveys", tags=["Surveys"])
appServer.include_router(user.router, prefix="/api/v1", tags=["Users"])

appServer.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@appServer.post("/api/v1/db-reset/")
async def reset_database():
    await Database.reset_database()
    return {"message": "Database reset successfully"}

@appServer.get("/")
async def healthcheck():
    return {"status": "ok"}
