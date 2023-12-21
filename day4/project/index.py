from fastapi import FastAPI

from day4.project.routes.main import user

app = FastAPI()

app.include_router(user)
