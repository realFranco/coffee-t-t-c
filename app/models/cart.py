from pydantic import BaseModel


class CartModel(BaseModel):
    id: str = None
