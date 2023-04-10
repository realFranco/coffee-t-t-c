"""
Coffee shop.

As we are using FastApi, here will be some quick ref. about the endpoints that will be working.

http://127.0.0.1:8004/docs

http://127.0.0.1:8004/redoc

uvicorn main:app --reload
"""
from fastapi import FastAPI

from app.api.cart import cart
from app.api.order import order


app = FastAPI()

# Include the rest of the routers.
app.include_router(cart)
app.include_router(order)


@app.get("/")
def coffee_shop():
    return {
        "info": "Coffee Shop from an e-commerce platform."
    }
