from extensions import db
from imports import *


class Cart(db.Model):
    __tablename__ = "cart"
    cart_id = db.Column(Integer, primary_key=True, autoincrement=True,
                        nullable=False)
    fk_user_id = db.Column(Integer,
                           ForeignKey("user.user_id", ondelete='RESTRICT'),
                           nullable=False)
    fk_order_id = db.Column(Integer,
                           ForeignKey("order.order_id", ondelete='RESTRICT'),
                           nullable=True, default=None)

    cart_has_dosed = sqlalchemy.orm.relationship('CartHasDosed',
                                                 backref='cart_has_dosed_')
    order = sqlalchemy.orm.relationship('Order', backref='order_')

class CartHasDosed(db.Model):
    __tablename__ = "cart_has_dosed"

    fk_cart_id = db.Column(Integer,
                           ForeignKey("cart.cart_id", ondelete='RESTRICT'),
                           primary_key=True,
                           nullable=False)
    fk_dosed_id = db.Column(Integer,
                            ForeignKey("dosed.dosed_id", ondelete='RESTRICT'),
                            primary_key=True,
                            nullable=False)

    dosed = sqlalchemy.orm.relationship('Dosed', backref='dosed_cart')
