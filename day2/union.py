from fastapi import FastAPI, Query
from typing import Union

app = FastAPI()

# Query Parameter
@app.get("/query")
def query_fun1(name: str, roll_no: int | None = None):
    person = {"name": name, "roll no": roll_no}
    return person


@app.get("/query/union")
def query_fun2(name: str, roll_no: Union[int, None] = Query(default=None)):
    person = {"name": name, "roll no": roll_no}
    return person
