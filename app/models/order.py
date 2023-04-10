from pydantic import BaseModel

from app.config.constants import Constants


class OrderModel(BaseModel):
    id: int 
    cart_id: int
    ttl_products: float = 0
    ttl_discounts: float = 0
    ttl_shipping: float = float(Constants.DEFAULT_SHIPPING_PRICE)
    order: float = 0
