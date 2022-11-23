from marshmallow import validate, fields
from extensions import ma

from ..cart.schema import CartSchema
from ..user.schema import UserSchemaGet


class OrderSchema(ma.Schema):
    date_of_purchase = fields.Date(required=True)
    total = fields.Float()

    fk_cart_id = fields.Integer(load_only=True, required=True)
    fk_user_id = fields.Integer(load_only=True, required=True)

    user = fields.Nested(UserSchemaGet, dump_only=True)
    cart = fields.Nested(CartSchema, dump_only=True)


class OrderSchemaGet(ma.Schema):
    fk_user_id = fields.Integer(load_only=True, required=True)

    date_of_purchase = fields.Date(dump_only=True)
    total = fields.Float(dump_only=True)
    cart = fields.Nested(CartSchema, dump_only=True)


class OrderSchemaUpdate(ma.Schema):
    fk_user_id = fields.Integer(load_only=True, required=True)
    fk_cart_id = fields.Integer(load_only=True)
    # fk_undosed_id = fields.Integer(load_only=True)

    cart = fields.Nested(CartSchema, dump_only=True)


class UserGetId(ma.Schema):
    fk_user_id = fields.Integer(load_only=True, required=True)
