from marshmallow import validate, fields
from extensions import ma


class UserSchema(ma.Schema):
    email = fields.Email(required=True)
    phone = fields.Integer(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class UserSchemaGet(ma.Schema):
    email = fields.Str(dump_only=True)

class UserSchemaUpdate(ma.Schema):
    class Meta:
        fields = ("first_name", "last_name")
