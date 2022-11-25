from marshmallow import validate, fields
from extensions import ma


class UserSchema(ma.Schema):
    email = fields.Email(required=True)
    phone = fields.Integer(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True,
                          validate=validate.Length(min=8, max=15))


class UserSchemaGet(ma.Schema):
    email = fields.Str(dump_only=True)


class UserSchemaUpdate(ma.Schema):
    class Meta:
        fields = ("first_name", "last_name")


class UserLoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True,
                          validate=validate.Length(min=8, max=15))
