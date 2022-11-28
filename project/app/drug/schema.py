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

    sub_category = fields.Nested(SubCategorySchema, dump_only=True)
    producer = fields.Nested(ProducerSchema, dump_only=True)


class DosedSchemaUpdate(ma.Schema):
    dosed_name = fields.Str(required=True,
                            validate=validate.Length(min=4, max=30))
    dosed_description = fields.Str(required=True,
                                   validate=validate.Length(min=20, max=500))


class DosedSchemaGet(ma.Schema):
    dosed_name = fields.Str(dump_only=True)
    dosed_description = fields.Str(dump_only=True)
    dosed_price = fields.Float(dump_only=True)



class UserGetId(ma.Schema):
    fk_user_id = fields.Integer(load_only=True, required=True)


class DetailsSchema(Schema):
    quantity = fields.Integer(validate=validate.Range(min=1), required=True)
    custom_id = fields.Integer(validate=validate.Range(min=1), required=True)
    menu_id = fields.Integer(validate=validate.Range(min=1), required=True)


class CustomSchema(Schema):
    id = fields.Integer(validate=validate.Range(min=0))
    price = fields.Float(validate=validate.Range(min=0), required=True)
    time = fields.DateTime(format='%Y-%m-%dT%H:%M:%S',
                           default=datetime.datetime.now(),
                           validate=lambda x: x <= datetime.datetime.now())
    status = fields.Str(dump_default='registered',
                        validate=validate.OneOf(['registered', 'processed', 'accepted',
                                                'prepared', 'delivered', 'done', 'cancelled']),
                        required=False)
    address_id = fields.Integer(validate=validate.Range(min=0), required=True)
    user_id = fields.Integer(validate=validate.Range(min=0), required=True)
    # details = fields.Dict(fields.Str(), fields.Integer()), required=True)
    # details = fields.List(fields.Nested(DetailsSchema()), many=True, required=True)
    # details = fields.List(fields.Str(), required=True)