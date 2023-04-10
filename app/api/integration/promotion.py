from sqlalchemy import func

from app.orm.db_connection import session
from app.orm.schemas.product import Product, Category
from app.orm.schemas.prods_in_cart import ProdsInCart
from app.orm.schemas.cart import Cart


class Promotion:
    COFFEE_THRESHOLD: int = 2
    EQUIPMENT_THRESHOLD: int = 3
    EQUIPMENT_PROPORTION_DISCOUNT: float = 10
    ACCESSORIES_THRESHOLD: int = 70

    @staticmethod
    def product_categories_at_cart(session: session, cart_id: int, category: Category) -> int:        
        return session.query(func.sum(ProdsInCart.quantity)) \
            .join(Product, ProdsInCart.product_id == Product.id) \
            .join(Cart, ProdsInCart.cart_id == Cart.id) \
            .filter(Cart.id==cart_id, Product.category==category).scalar()
    
    @staticmethod
    def is_extra_coffee_available(session: session, cart_id: int) -> bool:
        if Promotion.product_categories_at_cart(session, cart_id, Category.coffee) >= Promotion.COFFEE_THRESHOLD:
            return True
        
        return False
    
    @staticmethod
    def is_free_shipping_available(session: session, cart_id: int) -> bool:
        equipment_at_cart = Promotion.product_categories_at_cart(session, cart_id, Category.equipment)
        if None != equipment_at_cart and equipment_at_cart > Promotion.EQUIPMENT_THRESHOLD:
            return True

        return False

    @staticmethod
    def get_equipment_discount(session: session, cart_id: int) -> float:
        """
        Return the total discount on equipment.

        If return `x`, means that the total price to be payed will be `total - x`.
        """
        equipment = session.query(Product.price, ProdsInCart.quantity) \
            .join(ProdsInCart, Product.id == ProdsInCart.product_id) \
            .join(Cart, ProdsInCart.cart_id == Cart.id) \
            .filter(Cart.id==cart_id, Product.category==Category.equipment).all()
        
        if None != equipment:
            total_equipment = sum([ equip[0] * equip[1] for equip in equipment ])
            if total_equipment >= Promotion.ACCESSORIES_THRESHOLD:
                return total_equipment * (Promotion.EQUIPMENT_PROPORTION_DISCOUNT / 100)
        
        return 0
