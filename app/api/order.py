"""
Order router.
"""
import traceback

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import SessionTransaction
from starlette.responses import JSONResponse
from sqlalchemy import func

from app.config.constants import Tags, Msg
from app.config.routes import Routes
from app.orm.db_connection import session
from app.orm.schemas.cart import Cart
from app.orm.schemas.product import Product, Category
from app.orm.schemas.prods_in_cart import ProdsInCart
from app.api.integration.promotion import Promotion
from app.models.product import ProductToCartModel


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

        # @todo: If `cartId` it is currently related with an `Order` row, return 400 & a message.

        if True == Promotion.is_extra_coffee_available(session, cartId):
            coffee = session.query(ProdsInCart.product_id, ProdsInCart.quantity) \
                .join(Product, Product.id == ProdsInCart.product_id) \
                .join(Cart, Cart.id == ProdsInCart.cart_id) \
                .where(Cart.id == cartId, Product.category==Category.coffee).first()
            
            # The `coffee` tuple has to values, `ProdsInCart.product_id` and `ProdsInCart.quantity`.
            session.query(ProdsInCart)\
                .filter(ProdsInCart.cart_id==cartId, ProdsInCart.product_id==coffee[0])\
                .update({'quantity': coffee[1] + 1})

        # @todo: Continue with the promotions.
        # Promotion.is_free_shipping_available(session, cartId)
        # Promotion.is_discount_available(session, cartId)

        # @todo: Enable the `commit` statement after completes the endpoint.
        # session.commit()

        return {
            'coffee': True
        }
    
    except Exception as err:
        traceback.print_exc()
        print(f'At create the Order: {str(err)}')

        return JSONResponse(status_code=400, content={'error': str(err)})
