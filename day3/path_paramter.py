from fastapi import FastAPI, Query, Path

app = FastAPI()

# Order matter of defining routes
# if we are defining path with /items/me and /items/{id} then put /items/me first otherwise it can conside this route /items/{id}
# and take 'id' as 'me' and me can't be convert to string so it give error
@app.get("/items/me")
async def list_item():
    return {"hello! it's me"}


@app.get("/items/{id}")
async def list_item(id: int):
    return {"id": id, "item": f"item_{id}"}

# Path Parameters and numeric validation
@app.get("/items_validation/{item_id}")
async def read_item(item_id: int = Path(..., title="The ID of the item to get", gt=10, le=100)):
    res = {"item_id": item_id}
    return res

