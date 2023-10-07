from sqlalchemy.orm.session import SessionTransaction

from app.orm.schemas.cart import Cart as CartSchema


class Cart:

    @staticmethod
    def get_cart_by_id(id: int, session: SessionTransaction):
        return session.query(CartSchema).filter(CartSchema.id == id).first()
