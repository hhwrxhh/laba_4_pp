from marshmallow import validate, fields
from extensions import ma
from ..category.schema import SubCategorySchema
from ..producer.schema import ProducerSchema


class DosedSchema(ma.Schema):
    dosed_id = fields.Integer()
    dosed_name = fields.Str(required=True,
                            validate=validate.Length(min=4, max=30))
    dosed_description = fields.Str(required=True,
                                   validate=validate.Length(min=20, max=500))
    dosed_form = fields.Str(validate=validate.OneOf(
        ["capsules", "pills", "dragee", "granules", "powders",
         "solutions",
         "infusions",
         "tinctures", "liquid extracts", "emulsions", "mixtures"]),
        required=True)
    physical_form = fields.Str(validate=validate.OneOf(["solid", "liquid"]),
                               required=True)
    the_number_of_blisters = fields.Integer()
    quantity_in_package = fields.Integer()
    net_weight = fields.Float(required=True)
    unit_of_measurement = fields.Str(
        validate=validate.OneOf(["ml", "l", "mg", "gr"]),
        required=True)
    for_a_prescription = fields.Str(validate=validate.OneOf(["true", "false"]))
    dosed_price = fields.Float(required=True,
                               validate=validate.Range(min=0, max=10000))

    fk_producer_id = fields.Integer(load_only=True, required=True)
    fk_sub_category_id = fields.Integer(load_only=True, required=True)
    fk_user_id = fields.Integer(load_only=True, required=True)

    sub_category = fields.Nested(SubCategorySchema, dump_only=True)
    producer = fields.Nested(ProducerSchema, dump_only=True)


class DosedSchemaUpdate(ma.Schema):
    dosed_name = fields.Str(required=True,
                            validate=validate.Length(min=4, max=30))
    dosed_description = fields.Str(required=True,
                                   validate=validate.Length(min=20, max=500))
    fk_user_id = fields.Integer(load_only=True, required=True)


class DosedSchemaGet(ma.Schema):
    dosed_name = fields.Str(dump_only=True)
    dosed_description = fields.Str(dump_only=True)
    dosed_price = fields.Float(dump_only=True)

    fk_user_id = fields.Integer(load_only=True, required=True)


class UserGetId(ma.Schema):
    fk_user_id = fields.Integer(load_only=True, required=True)
