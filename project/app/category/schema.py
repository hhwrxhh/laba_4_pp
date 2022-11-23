from marshmallow import validate, fields
from extensions import ma


class CategorySchema(ma.Schema):
    category_id = fields.Integer(required=True, dump_only=True)
    category_name = fields.Str(required=True,
                               validate=validate.Length(min=4, max=30))


class SubCategorySchema(ma.Schema):
    sub_category_id = fields.Integer(required=True, dump_only=True)
    sub_category_name = fields.Str(required=True,
                                   validate=validate.Length(min=4, max=30))
    fk_category_id = fields.Integer(load_only=True, required=True)

    category = fields.Nested(CategorySchema, dump_only=True)


class SubCategorySchemaUpdate(ma.Schema):
    sub_category_name = fields.Str(required=True,
                                   validate=validate.Length(min=4, max=30))

    category = fields.Nested(CategorySchema, dump_only=True)



