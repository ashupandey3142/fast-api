from pydantic import BaseModel, Field, EmailStr
from fastapi import FastAPI
from typing import Literal

app = FastAPI()


class Image(BaseModel):
    url: str = Field(...,
                     regex="^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)$")
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []
    img: Image


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    res = {"item_id": item_id, "item": item}
    return res


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


# Response model -> required for doc purpose, generally to declare the return type
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str


class UserIn(UserBase):
    password: Field(..., regex='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$')


class UserOut(UserBase):
    pass


@app.post("/users", response_model=UserOut)
async def create_user(user: UserIn):
    return user


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: Literal["foo", "bar", "baz"]):
    return items[item_id]


@app.get("/items/{item_id}/name", response_model=Item, response_model_include={"name", "description"})
async def read_item(item_id: Literal["foo", "bar", "baz"]):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item(item_id: Literal["foo", "bar", "baz"]):
    return items[item_id]


# Extra model
class UserInDB(BaseModel):
    username: str
    hash_pass: str
    email: EmailStr
    full_name: str | None = None


def fake_hash_pass(raw_pass: str):
    return f"secret{raw_pass}"


def fake_save_pass(user_in: UserIn):
    hash_pass = fake_hash_pass(user_in.password)
    db_user = UserInDB(**user_in.model_dump(), hash_pass=hash_pass)
    print("user_in", user_in.model_dump())
    print("User saved")
    return db_user


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    save_user = fake_save_pass(user_in)
    return save_user
