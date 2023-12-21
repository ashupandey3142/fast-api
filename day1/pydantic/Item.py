from typing import List
from pydantic import BaseModel, EmailStr, field_validator
from fastapi import FastAPI

app = FastAPI()
# Item is a Pydantic model that defines the structure of the data expected in the request body.
# It has two required fields (name, price) and two optional fields (description, tax).

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = 0.0
    tags: List[str] = []

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) < 3:
            raise ValueError("Name must be at least 3 characters long")
        return value.capitalize()


class User(BaseModel):
    username: str
    email: EmailStr


class Order(BaseModel):
    items: List[Item]
    user: User


# Example usage
item_data = {"name": "apple", "price": 2.5}
item = Item(**item_data)
print(item)

order_data = {
    "items": [item_data, {"name": "banana", "price": 1.5}],
    "user": {"username": "john_doe", "email": "john@example.com"}
}
order = Order(**order_data)
print(order)


# The create_item function is a FastAPI route that accepts a POST request at the "/items/" endpoint.
# The request body is automatically parsed into an Item instance based on the Pydantic model.
@app.post("/items/")
async def create_item(item: Item):
    return item
