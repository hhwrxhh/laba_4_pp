from marshmallow import validate, fields
from extensions import ma

from ..drug.schema import DosedSchema
from ..drug.schema import DosedSchemaGet

class CartSchema(ma.Schema):
    fk_dosed_id = fields.Integer(load_only=True)
    fk_undosed_id = fields.Integer(load_only=True)
    cart_id = fields.Integer(dump_only=True)

    dosed = fields.Nested(DosedSchemaGet, dump_only=True)


class CartSchemaGet(ma.Schema):
    fk_dosed_id = fields.Integer(load_only=True)
    fk_undosed_id = fields.Integer(load_only=True)

    dosed = fields.Nested(DosedSchemaGet, dump_only=True)


class CartSchemaUpdate(ma.Schema):
    fk_dosed_id = fields.Integer(load_only=True)

    dosed = fields.Nested(DosedSchemaGet, dump_only=True)
