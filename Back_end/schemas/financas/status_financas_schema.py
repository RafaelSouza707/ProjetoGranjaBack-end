from marshmallow import Schema, fields, EXCLUDE, validate

class StatusFinancasSchema(Schema):
    id = fields.Integer(dump_only=True)

    nome = fields.String(required=True, validate=validate.Length(max=32))

class Meta:
    unknown = EXCLUDE