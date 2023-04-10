import traceback

from sqlalchemy import Column, Integer, ForeignKey, Float

from app.orm.db_connection import Base
from app.models.order import OrderModel
from app.config.constants import Constants


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('cart.id'))
    ttl_products = Column(Float, default=float(0), nullable=False)
    ttl_discounts = Column(Float, default=float(0), nullable=False)
    ttl_shipping = Column(Float, default=float(Constants.DEFAULT_SHIPPING_PRICE), nullable=False)

    def to_model(self) -> OrderModel:
        try:
            return OrderModel(
                id=self.id,
                cart_id=self.cart_id,
                ttl_products=self.ttl_products,
                ttl_discounts=self.ttl_discounts,
                ttl_shipping=self.ttl_shipping,
                order=(self.ttl_products + self.ttl_shipping) - self.ttl_discounts
            )

        except Exception as err:
            traceback.print_exc()
            print(f'At Order to model: {str(err)}')

            return None

    def format(self) -> bool:
        try:
            self.ttl_products = float(Constants.FLOAT_FORMAT % self.ttl_products)
            self.ttl_discounts = float(Constants.FLOAT_FORMAT % self.ttl_discounts)
            self.ttl_shipping = float(Constants.FLOAT_FORMAT % self.ttl_shipping)

            return True

        except Exception as err:
            traceback.print_exc()
            print(f'At Order parse: {str(err)}')

            return False
