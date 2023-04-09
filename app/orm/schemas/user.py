import random
import traceback

from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from app.orm.db_connection import Base
from app.models.cart import CartModel
from app.config.constants import Constants


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    carts = relationship('Cart', back_populates='user', lazy='dynamic')
    
    def parse(self, cart: CartModel) -> bool:
        try:
            self.id = cart.id if cart.id else random.randint(1, Constants.MAX_RAND_INT)

            return True
        
        except Exception as err:
            traceback.print_exc()
            print(f'At user parse: {str(err)}')

            return False
