from pydantic import BaseModel
from typing import Union
from fastapi import Query
# Schema refers to the structure and validation rules applied to the data that your API expects in requests and sends in responses.
# in FastAPI, a schema is essentially a Pydantic model that defines the structure, data types, and validation rules for your API's input and output data.
# The terms "schema," "Pydantic model," and "FastAPI model" are often used interchangeably in the context of FastAPI development.


class Schema1(BaseModel):
    name: str
    roll_no: str = Query(default=None, min_length=2, max_length=4)
    subject: Union[str, None] = None


# Nested Model
class Image(BaseModel):
    url: str
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]
