from pydantic import BaseModel


class OrderModel(BaseModel):
    id: int 
    cart_id: int
    ttl_products: float = 0
    ttl_discounts: float = 0
    ttl_shipping: float = 0
