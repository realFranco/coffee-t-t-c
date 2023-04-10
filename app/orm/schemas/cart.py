import traceback
import random

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.orm.db_connection import Base
from app.models.cart import CartModel
from app.config.constants import Constants
from app.orm.schemas.user import User


class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, back_populates='carts')

    products = relationship('Product', secondary="prods_in_cart", back_populates='carts', lazy='joined')


    def parse(self, cart: CartModel) -> bool:
        try:
            self.id = cart.id if cart.id else random.randint(1, Constants.MAX_RAND_INT)
            self.user_id = cart.user_id 

            return True
        
        except Exception as err:
            traceback.print_exc()
            print(f'At cart parse: {str(err)}')

            return False
