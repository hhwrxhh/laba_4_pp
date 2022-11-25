from extensions import db
from imports import *


class Cart(db.Model):
    __tablename__ = "cart"
    cart_id = db.Column(Integer, primary_key=True, autoincrement=True,
                        nullable=False)
    fk_dosed_id = db.Column(Integer,
                            ForeignKey("dosed.dosed_id", ondelete='RESTRICT'),
                            nullable=True, default=None)
    fk_user_id = db.Column(Integer,
                           ForeignKey("user.user_id", ondelete='RESTRICT'),
                           nullable=False)

    dosed = sqlalchemy.orm.relationship('Dosed', backref='dosed_')
    user = sqlalchemy.orm.relationship('User', backref='user_')
