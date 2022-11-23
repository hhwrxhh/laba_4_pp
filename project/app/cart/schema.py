from marshmallow import validate, fields
from extensions import ma

from ..drug.schema import DosedSchema
from ..drug.schema import DosedSchemaGet

class CartSchema(ma.Schema):
    fk_user_id = fields.Integer(load_only=True, required=True)
    fk_dosed_id = fields.Integer(load_only=True)
    fk_undosed_id = fields.Integer(load_only=True)

    dosed = fields.Nested(DosedSchemaGet, dump_only=True)


class CartSchemaGet(ma.Schema):
    fk_user_id = fields.Integer(load_only=True, required=True)
    fk_dosed_id = fields.Integer(load_only=True)
    fk_undosed_id = fields.Integer(load_only=True)

    dosed = fields.Nested(DosedSchemaGet, dump_only=True)


class CartSchemaUpdate(ma.Schema):
    fk_user_id = fields.Integer(load_only=True, required=True)
    fk_dosed_id = fields.Integer(load_only=True)

    dosed = fields.Nested(DosedSchemaGet, dump_only=True)


class UserGetId(ma.Schema):
    fk_user_id = fields.Integer(load_only=True, required=True)