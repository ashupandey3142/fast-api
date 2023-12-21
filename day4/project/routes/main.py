from fastapi import APIRouter

from day4.project.config.db import con
from day4.project.models.index import users
from day4.project.schema.index import User

user = APIRouter()


@user.get("/")
async def read_data():
    return con.execute(users.select()).fetchall()


@user.get("/{id}")
async def read_data(id: int):
    return con.execute(users.select().where(users.c.id == id)).fetchall()


@user.post("/")
async def write_data(user: User):
    con.execute(users.insert().values(
        id=user.id,
        name=user.name,
        email=user.email,
        password=user.password
    ))
