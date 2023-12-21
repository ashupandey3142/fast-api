from fastapi import FastAPI, Query

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}, {"item_name": "Bear"},
                 {"item_name": "Blade"}, {"item_name": "Black"}]


# As query parameters are not a fixed part of a path, they can be optional and can have default values.
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]  # slicing


# Pydantic Type conversion
@app.get("/items/{item_id}")
async def get_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({
                        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged."})
    return item


# Multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
        user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# Required query parameters
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item


# Query parameter with string validation
# Optional Parameter
@app.get("/item/optional")
async def read_items(q: str | None = Query(default=None, min_length=2, max_length=20, regex="^the.*many$")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Required Parameter
@app.get("/item/required")
async def read_items(q: str = Query(..., min_length=2, max_length=20, regex="^the.*many$")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# If we want to allow multiple query parameter
@app.get("/item/multiple")
async def read_items(
        q: list[str]
           | None = Query(
            None,
            min_length=2,
            max_length=20,
            regex="^the.*many$",
            description="This will tell the description of the particular parameter",
        )):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# In python we can't create query parameter like post-q, python allows snake case only
# @app.get("/items/restriction")
# async def read_items(post-q: str = Query(..., min_length=2, max_length=20, regex="^the.*many$")):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results
# Sp for allowing we have alias attribute
@app.get("/item/restriction")
async def read_items(
        q: str | None = Query(None, alias="post-title")):  # now the query pramter act as post-title not as q
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/item/hidden")
async def hidden_query(que: str | None = Query(None, include_in_schema=False)):
    if que:
        return {"Hidden-Query": que}
    return {"Hidden-Query": "Not found"}
