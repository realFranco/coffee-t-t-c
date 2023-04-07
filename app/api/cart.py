"""
Cart router.
"""
import traceback

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import SessionTransaction

from app.config.constants import Tags, Msg
from app.config.routes import Routes
from app.orm.db_connection import session
from app.orm.cart import Cart
from app.models.cart import CartModel


cart = APIRouter(
    prefix=Routes.CART,
    tags=[Tags.cart],
    responses={404: Msg.NOT_FOUND},
)

"""
    ------- Cart section ------- 

    GET: http://127.0.0.1:8004/cart/
"""
@cart.get('/', tags=[Tags.cart])
async def get_cart(session: SessionTransaction = Depends(session)):
    """
    Get a cart.
    """
    return {
        "id": 123,
        "title": "Init Coffee shop"
    }
