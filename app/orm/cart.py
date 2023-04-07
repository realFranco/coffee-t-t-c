from sqlalchemy import Column, String, Integer

from app.orm.db_connection import Base
# from app.models.cart import CartModel


class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, unique=True)
