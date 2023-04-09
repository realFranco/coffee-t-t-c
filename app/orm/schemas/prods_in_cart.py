from sqlalchemy import Column, Integer, ForeignKey

from app.orm.db_connection import Base



class ProdsInCart(Base):
    __tablename__ = "prods_in_cart"
    quantity = Column(Integer, default=int(0), nullable=False)

    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    cart_id = Column(Integer, ForeignKey('cart.id'), primary_key=True)
    quantity = Column(Integer)


    # def parser(self, product: )