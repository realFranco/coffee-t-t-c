from typing import List, Union

from sqlalchemy.orm.session import SessionTransaction
from starlette.responses import JSONResponse

# from app.orm.schemas.cart import Cart as CartSchema
from app.models.product import ProductToCartModel
from app.repository.Cart import Cart as CartRepository
from app.orm.schemas.product import Product as ProductSchema


class Cart:

    @staticmethod
    def get_cart_by_id(id: int, session: SessionTransaction) -> dict:
        """
        Given an identifier, collect a Cart entity related to it.
        
        :param id int. Cart identifier.
        :param session SessionTransaction. Session to be used during query.

        :return The cart object specified.
        """
        cart = CartRepository.get_cart_by_id(id, session)
        if None == cart:
            return JSONResponse(
                status_code=404, 
                content={'error': f'Cart "{id}" do not exist.'}
            )

        return {'cart': cart}


    @staticmethod
    def get_cart_by_product_ids(products: List[ProductToCartModel], 
                                session: SessionTransaction) -> Union[List[tuple[int]], List]:
        """
        Given a list of products use the identifier and return the Product entities related to it.

        :param products List[ProductToCartModel]. List of products that are related with carts.
        :param session SessionTransaction. Session to be used during query.

        :return The identifier for each product.
        """
        # @todo: Implement the repository layer.
        return session.query(ProductSchema.id)\
            .filter(
                ProductSchema.id.in_([ prod.product_id for prod in products ])
            )\
            .all()
