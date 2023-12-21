# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

db = []

# Model for the data
class Item(BaseModel):
    name: str
    description: Optional[str] = None


# Create operation
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    db.append(item)
    return item

# Read operation
@app.get("/items/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 10):
    return db[skip : skip + limit]

# Read single item operation
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    if item_id < 0 or item_id >= len(db):
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]

# Update operation
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    if item_id < 0 or item_id >= len(db):
        raise HTTPException(status_code=404, detail="Item not found")
    db[item_id] = item
    return item

# Delete operation
@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    if item_id < 0 or item_id >= len(db):
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = db.pop(item_id)
    return deleted_item
