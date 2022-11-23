from marshmallow import validate, fields
from extensions import ma

class ProducerSchema(ma.Schema):
    producer_id = fields.Integer()
    producing_company = fields.Str(required=True,
                                   validate=validate.Length(min=4, max=30))
    producing_country = fields.Str(required=True,
                                   validate=validate.Length(min=4, max=30))
