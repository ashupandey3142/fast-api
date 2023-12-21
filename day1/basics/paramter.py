from fastapi import FastAPI
app = FastAPI()

# Path parameters with types
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Query Parameter
@app.get("/query")
# all parameter required
def query_fun(name: str, roll_no: int):
    var_name = {"name": name, "roll no": roll_no}
    return var_name

@app.get("/query2")
# name is required parameter and roll no is optional
def query_fun2(name: str, roll_no: int | None = None):
    var_name = {"name": name, "roll no": roll_no}
    return var_name
