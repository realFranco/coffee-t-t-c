from pydantic import BaseModel


class ProductModel(BaseModel):
    id: int = None
    name: str = None
    price: float = None
    category: str = None


class ProductToCartModel(BaseModel):
    product_id: int
    quantity: int = 0
    