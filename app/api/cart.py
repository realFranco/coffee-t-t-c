"""
Cart router.
"""
import traceback
from typing import Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import SessionTransaction
from starlette.responses import JSONResponse

from app.config.constants import Tags, Msg
from app.config.routes import Routes
from app.orm.db_connection import session
from app.orm.schemas.cart import Cart
from app.orm.schemas.prods_in_cart import ProdsInCart
from app.models.product import ProductToCartModel
from app.controller.Cart import Cart as CartController
from app.controller.User import User as UserController


cart = APIRouter(
    prefix=Routes.CART,
    tags=[Tags.cart],
    responses={404: Msg.NOT_FOUND},
)

@cart.get('/', tags=[Tags.cart])
async def get_cart(id: int, session: SessionTransaction = Depends(session)):
    """Get a Cart by id."""
    try:
        prods_in_cart = CartController.get_cart_by_id(id=id, session=session)

        # @todo: Create a new endpoint to return products with quantity.
        # @info: Why the products with quantity are required?

        return prods_in_cart
                
    except Exception as err:
        traceback.print_exc()
        print(f'At get Cart: {str(err)}')

        return JSONResponse(status_code=400, content={'error': str(err)})


@cart.post('/', tags=[Tags.cart])
async def create_cart(userId: int,
                      session: SessionTransaction = Depends(session)):
    """Create a Cart."""
    try:
        if None == UserController.get_user_by_id(id=userId, session=session):
            return JSONResponse(
                status_code=404, 
                content={'error': f'User "{userId}" do not exist.'}
            )

        n_cart = Cart(user_id=userId)
        session.add(n_cart)
        session.commit()
        session.refresh(n_cart)
    
        return n_cart

    except Exception as err:
        session.rollback()
        traceback.print_exc()
        print(f'At create cart: {str(err)}')

        return JSONResponse(status_code=400, content={'error': str(err)})


@cart.post('/{cartId}/products', tags=[Tags.cart])
async def add_products_to_cart(cartId: int,
                                products: List[ProductToCartModel],
                                session: SessionTransaction = Depends(session)) -> Dict[str, int]:
    """
    Add Products to Cart.
    
    The products to be inserted will be verified before related with the final cart.

    You could ony add the product once, if you want to edit the quantity of the product, 
    use the update operation instead.
    """
    try:
        if None == CartController.get_cart_by_id(id=cartId, session=session):
            return JSONResponse(
                status_code=404, 
                content={'error': f'Cart "{cartId}" do not exist.'}
            )
        
        # Retrieve valid only products (already stored products).
        products_registered = CartController\
            .get_cart_by_product_ids(products=products, session=session)
        if [] == products_registered:
            return JSONResponse(
                status_code=404, 
                content={'error': f'Products to insert do not exist.'}
            )
        products_registered = [_[0] for _ in products_registered] if products_registered else []

        add_counter: int = 0
        for prod in products:
            if prod.product_id in products_registered:
                # Verify if the combination Product and Cart not exist before execute an insertion operation.
                if None == session.query(ProdsInCart)\
                    .filter(ProdsInCart.product_id==prod.product_id, ProdsInCart.cart_id==cartId).first():
                    session.add(
                        ProdsInCart(product_id=prod.product_id, cart_id=cartId, quantity=prod.quantity)
                    )
                    add_counter += 1
        session.commit()

        # @todo: Add a model or interface to define this data type.
        return {
            'productsRegistered': add_counter
        }

    except Exception as err:
        session.rollback()
        traceback.print_exc()
        print(f'At adding Products to Cart: {str(err)}')

        return JSONResponse(status_code=400, content={'error': str(err)})


@cart.put('/{cartId}/', tags=[Tags.cart])
async def set_quantity_products_inside_a_cart(cartId: int, 
                                                products: List[ProductToCartModel],
                                                session: SessionTransaction = Depends(session)):
    """Modify the Product quantity inside a Cart."""
    try:
        if None == CartController.get_cart_by_id(id=cartId, session=session):
            return JSONResponse(
                status_code=404, 
                content={'error': f'Cart "{cartId}" do not exist.'}
            )

        prods_in_cart = session.query(ProdsInCart.product_id)\
            .filter(ProdsInCart.cart_id==cartId).all()
        if [] == prods_in_cart:
            return JSONResponse(
                status_code=400, 
                content={'error': f'The Cart "{cartId}" do not contain Products to modify.'}
            )

        prods_in_cart = [_[0] for _ in prods_in_cart]
        add_counter = 0
        for product in products:
            if product.product_id in prods_in_cart:
                if 0 == product.quantity:
                    # If a Product quantity is 0, execute a `delete()` operation at the Cart.
                    session.query(ProdsInCart)\
                        .filter(ProdsInCart.cart_id==cartId, ProdsInCart.product_id==product.product_id)\
                        .delete()
                    add_counter += 1
                else:
                    # Modify Products related with the Cart.
                    session.query(ProdsInCart)\
                        .filter(ProdsInCart.cart_id==cartId, ProdsInCart.product_id==product.product_id)\
                        .update({'quantity': product.quantity})
                    add_counter += 1

        session.commit()

        return {
            'productsModified': add_counter
        }

    except Exception as err:
        session.rollback()
        traceback.print_exc()
        print(f'At modifying the Products quantity inside a Cart: {str(err)}')

        return JSONResponse(status_code=400, content={'error': str(err)})        
