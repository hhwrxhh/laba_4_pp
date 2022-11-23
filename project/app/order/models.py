from extensions import db
from imports import *


class Order(db.Model):
    __tablename__ = "order"
    order_id = db.Column(Integer, primary_key=True, autoincrement=True,
                         nullable=False)
    fk_user_id = db.Column(Integer,
                           ForeignKey("user.user_id", ondelete='CASCADE'),
                           primary_key=True,
                           nullable=False)
    fk_cart_id = db.Column(Integer,
                           ForeignKey("cart.cart_id", ondelete='RESTRICT'),
                           nullable=False)
    date_of_purchase = db.Column(Date, nullable=False)
    total = db.Column(Float, nullable=False)
    user = sqlalchemy.orm.relationship('User')
    cart = sqlalchemy.orm.relationship('Cart')

    def __init(self, date_of_purchase, total):
        self.date_of_purchase = date_of_purchase
        self.total = total
