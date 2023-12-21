from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The foo"}

@app.get("/items/{item_id}")
async def read_items(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=204, detail="Item not found")
    return items[item_id]
