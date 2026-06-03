from marshmallow import Schema, fields, validate, EXCLUDE

class VendaSchema(Schema):
    id = fields.Integer(dump_only=True)

    nome = fields.String(required=True, validate=validate.Length(max=8))

class Meta:
    unknown = EXCLUDE