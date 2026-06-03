from marshmallow import Schema, fields, validate, EXCLUDE

class SexoSchema(Schema):
    id = fields.Integer(dump_only=True)

    nome = fields.String(required=True, validate=validate.Length(max=1))

class Meta:
    unknown = EXCLUDE