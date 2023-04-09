import enum

from sqlalchemy import Column, Integer, String, Float

from app.orm.db_connection import Base
from app.models.product import ProductModel
from sqlalchemy.orm import relationship
from app.orm.schemas.prods_in_cart import ProdsInCart



class Category(str, enum.Enum):
    accessories = 'accessories'
    coffee = 'coffee'
    equipment = 'equipment'


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, default=float(0), nullable=False)
    category = Column(String, nullable=True)

    carts = relationship('Cart', secondary="prods_in_cart", back_populates='products')

    def parse(self, product: ProductModel) -> bool:
        try:
            return True
        except Exception as error:
            return False