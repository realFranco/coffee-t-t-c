"""
Cart router.
"""
import traceback

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import SessionTransaction
from starlette.responses import JSONResponse

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
async def get_cart(id: str):
    """Get a cart."""
    try:
        return JSONResponse(
            status_code=200,
            content={"id": id, "title": "Init Coffee shop"}
        )

    except Exception as err:
        traceback.print_exc()
        print(f'At get cart: {str(err)}')

        return JSONResponse(status_code=400, content={'error': str(err)})

@cart.post('/', tags=[Tags.cart])
async def create_cart(cart: CartModel,
        session: SessionTransaction = Depends(session)):
    """Create a cart."""
    try:
        n_cart = Cart()
        if not n_cart.parse(cart):
            return JSONResponse(
                status_code=400, 
                content={'error': 'Parse error'}
            )

        session.add(n_cart)
        session.commit()
        session.refresh(n_cart)
    
        return n_cart

    except Exception as err:
        session.rollback()
        traceback.print_exc()
        print(f'At create cart: {str(err)}')

        return JSONResponse(status_code=400, content={'error': str(err)})
