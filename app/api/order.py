"""
Order router.
"""
import traceback

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import SessionTransaction
from starlette.responses import JSONResponse

from app.config.constants import Tags, Msg
from app.config.routes import Routes
from app.orm.db_connection import session


order = APIRouter(
    prefix=Routes.ORDER,
    tags=[Tags.order],
    responses={404: Msg.NOT_FOUND},
)

@order.post('/{cartId}', tags=[Tags.order])
async def create_an_order(cartId: int, session: SessionTransaction = Depends(session)):
    """Create an Order."""
    try:
        cart = session.query(Cart).filter(Cart.id == cartId).first()
        if None == cart:
            return JSONResponse(
                status_code=404, 
                content={'error': f'Cart "{id}" do not exist.'}
            )

        # Apply the Rules / Promotions
        # Logic decouple at `integration/` directory.

        return {
            'orderCreated': True
        }
    
    except Exception as err:
        traceback.print_exc()
        print(f'At create the Order: {str(err)}')

        return JSONResponse(status_code=400, content={'error': str(err)})
