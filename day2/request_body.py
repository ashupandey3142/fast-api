from fastapi import FastAPI
from pydantic import BaseModel
from day2.schema.schema import Schema1


class Employee(BaseModel):
    id: int
    name: str
    designation: str = "Intern"
    salary: int = 20000


app = FastAPI()


@app.post("/employee")
async def create_item(emp: Employee):
    return emp


@app.post("/items")
async def create_item(item: Schema1):
    item_dict = item.model_dump()
    if item.name:
        item_dict.update({"msg": 'hello '+item.name})
    return item_dict

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Schema1):
    return {"item_id": item_id, **item.model_dump()}


# Request body with query parameter
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Schema1, q: str | None = None):
    res = {"item_id": item_id, **item.model_dump()}
    if q:
        res.update({"q": q})
    return res
