from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from day5.project.routes.index import application as project_router

app = FastAPI()

app.include_router(project_router, prefix="/project")
