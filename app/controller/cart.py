from sqlalchemy.orm.session import SessionTransaction
from starlette.responses import JSONResponse

from app.orm.schemas.cart import Cart as CartSchema

class Cart:

    @staticmethod
    def get_cart_by_id(id: int, session: SessionTransaction):
        """
        Given an identifier, collect a Cart object related to it.
        
        :param id int. Cart identifier.
        :param session. Database session to be used for the database query.

        :return The cart object specified.
        """
        # TODO: This query must be move it into a repository layer in order to decouple the data infrastructure from the controller.
        cart = session.query(CartSchema).filter(CartSchema.id == id).first()
        if None == cart:
            return JSONResponse(
                status_code=404, 
                content={'error': f'Cart "{id}" do not exist.'}
            )

        return {'cart': cart}
