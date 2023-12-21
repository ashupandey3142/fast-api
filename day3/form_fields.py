from fastapi import FastAPI, Form
from pydantic import BaseModel


app = FastAPI()

class User(BaseModel):
    username: str
    password: str


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    print("password", password)
    return {"username": username}
