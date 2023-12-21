# FastAPI -> FastAPI is a modern, fast(high performance), web framework for building API's with python3.7+ based on standard python type hints
# Features:
# Fast, Fast to code, fewer bugs, short code and easy
#

from fastapi import FastAPI
# uvicorn main:app --reload
# Uvicorn is an ASGI (Asynchronous Server Gateway Interface) server that is used to run web applications and
# APIs built with frameworks like FastAPI, Starlette, and other ASGI-compatible frameworks.
# The command uvicorn main:app refers to:
#
# main: the file main.py (the Python "module").
# app: the object created inside of main.py with the line app = FastAPI().
# --reload: make the server restart after code changes. Only use for development.

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Path Parameters
@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

# Path parameters with types
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Order matters
