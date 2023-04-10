"""
Order router.
"""
import traceback
import random

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import SessionTransaction
from starlette.responses import JSONResponse

from app.config.constants import Tags, Msg
from app.config.routes import Routes
from app.orm.db_connection import session
from app.orm.schemas.cart import Cart
from app.orm.schemas.product import Product, Category
from app.orm.schemas.prods_in_cart import ProdsInCart
from app.orm.schemas.order import Order
from app.api.integration.promotion import Promotion
from app.models.product import ProductToCartModel
from app.config.constants import Constants


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

        order = session.query(Order).filter(Order.cart_id == cartId).first()
        if None != order:
            return JSONResponse(
                status_code=400, 
                content={'error': f'An Order it is currently related with the Cart "{cartId}".'}
            )

        if True == Promotion.is_extra_coffee_available(session, cartId):
            coffee = session.query(ProdsInCart.product_id, ProdsInCart.quantity) \
                .join(Product, Product.id == ProdsInCart.product_id) \
                .join(Cart, Cart.id == ProdsInCart.cart_id) \
                .where(Cart.id == cartId, Product.category==Category.coffee).first()
            
            # The `coffee` tuple has to values, `ProdsInCart.product_id` and `ProdsInCart.quantity`.
            session.query(ProdsInCart)\
                .filter(ProdsInCart.cart_id==cartId, ProdsInCart.product_id==coffee[0])\
                .update({'quantity': coffee[1] + 1})

        new_order = Order(id=random.randint(1, Constants.MAX_RAND_INT), cart_id=cartId)

        # Calculate the price to be payed based on the Products selected.
        products_price_to_checkout = session.query(Product.price, ProdsInCart.quantity) \
            .join(ProdsInCart, Product.id == ProdsInCart.product_id) \
            .join(Cart, ProdsInCart.cart_id == Cart.id) \
            .filter(Cart.id==cartId).all()        
        new_order.ttl_products = sum([ prods[0] * prods[1] for prods in products_price_to_checkout ])

        if True == Promotion.is_free_shipping_available(session, cartId):
            new_order.ttl_shipping = 0

        new_order.ttl_discounts = Promotion.get_equipment_discount(session, cartId)

        # Ensure that the float digits be expressed in a readable way.
        if False == new_order.format():
            return JSONResponse(
                status_code=400, 
                content={'error': f'An error happens while format the Cart object.'}
            )

        # The `order` property will expose the money to be payed by the user and it is populated on-the-fly.
        order_model = new_order.to_model()
        if None == order_model:
            return JSONResponse(
                status_code=400, 
                content={'error': f'An error happens while generate the Order model object.'}
            )

        session.add(new_order)
        session.commit()

        return order_model
    
    except Exception as err:
        traceback.print_exc()
        print(f'At create the Order: {str(err)}')

        return JSONResponse(status_code=400, content={'error': str(err)})
