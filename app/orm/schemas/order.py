from sqlalchemy import Column, Integer, ForeignKey, Float

from app.orm.db_connection import Base


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('cart.id'))
    ttl_products = Column(Float, default=float(0), nullable=False)
    ttl_discounts = Column(Float, default=float(0), nullable=False)
    ttl_shipping = Column(Float, default=float(0), nullable=False)
