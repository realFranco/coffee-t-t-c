import traceback
import random

from sqlalchemy import Column, String, Integer

from app.orm.db_connection import Base
from app.models.cart import CartModel


class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, unique=True)

    def parse(self, cart: CartModel) -> bool:
        try:
            self.id = cart.id if cart.id else random.randint(1, 999)
            self.name = cart.name if cart.name else "Cart"

            return True
        
        except Exception as err:
            traceback.print_exc()
            print(f'At cart parse: {str(err)}')

            return False
