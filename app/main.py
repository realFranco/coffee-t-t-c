"""
Coffee shop.

As we are using FastApi, here will be some quick ref. about the endpoints that will be working.

http://127.0.0.1:8004/docs

http://127.0.0.1:8004/redoc

uvicorn main:app --reload
"""
from fastapi import FastAPI

from app.api.cart import cart


app = FastAPI()

# Include the rest of the routers
app.include_router(cart)

@app.get("/")
def read_root():
    return {"Hello": "World"}
