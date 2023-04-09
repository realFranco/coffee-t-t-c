"""
Cart router.
"""
import traceback
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import SessionTransaction
from starlette.responses import JSONResponse

from app.config.constants import Tags, Msg
from app.config.routes import Routes
from app.orm.db_connection import session
from app.orm.schemas.product import Product
from app.orm.schemas.cart import Cart
from app.orm.schemas.user import User
from app.orm.schemas.prods_in_cart import ProdsInCart
from app.models.product import ProductToCartModel


cart = APIRouter(
    prefix=Routes.CART,
    tags=[Tags.cart],
    responses={404: Msg.NOT_FOUND},
)

@cart.get('/', tags=[Tags.cart])
async def get_cart(id: int, session: SessionTransaction = Depends(session)):
    """Get a Cart by id."""
    try:
        cart = session.query(Cart).filter(Cart.id == id).first()
        if None == cart:
            return JSONResponse(
                status_code=404, 
                content={'error': f'Cart "{id}" do not exist.'}
            )

        prods_in_cart = session.query(ProdsInCart)\
            .filter(ProdsInCart.cart_id == id)\
            .all()

        return {
            'cart': cart,
            'productWithQuantity': {_.product_id: _.quantity for _ in prods_in_cart}
        }
                
    except Exception as err:
        traceback.print_exc()
        print(f'At get Cart: {str(err)}')

        return JSONResponse(status_code=400, content={'error': str(err)})

@cart.post('/', tags=[Tags.cart])
async def create_cart(userId: int,
        session: SessionTransaction = Depends(session)):
    """Create a Cart."""
    try:
        # Verify that the User exist before create a Cart row.
        if [] == session.query(User).filter(User.id == userId).first():
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
                                session: SessionTransaction = Depends(session)):
    """Add Products to Cart."""
    try:
        # Verify that the Cart exist before set Products.
        if [] == session.query(Cart).filter(Cart.id == cartId).first():
            return JSONResponse(
                status_code=404, 
                content={'error': f'Cart "{cartId}" do not exist.'}
            )
        
        # Filter the products that exist into the database.
        products_registered = session.query(Product.id)\
            .filter(
                Product.id.in_([ prod.product_id for prod in products ])
            )\
            .all()
        products_registered = [_[0] for _ in products_registered] if products_registered else []
        if [] == products_registered:
            return JSONResponse(
                status_code=404, 
                content={'error': f'Products to insert do not exist.'}
            )

        add_counter = 0
        for prod in products:
            if prod.product_id in products_registered:
                # Check if the combination Product | Cart not exist before execute an insert.
                if None == session.query(ProdsInCart)\
                    .filter(ProdsInCart.product_id==prod.product_id, ProdsInCart.cart_id==cartId).first():
                    session.add(
                        ProdsInCart(product_id=prod.product_id, cart_id=cartId, quantity=prod.quantity)
                    )
                    add_counter += 1
        session.commit()

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
        # Verify that the Cart exist before set Products.
        if [] == session.query(Cart).filter(Cart.id == cartId).first():
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
