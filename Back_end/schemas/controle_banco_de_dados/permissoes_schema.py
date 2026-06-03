from marshmallow import Schema, fields, EXCLUDE, validate

class PermissoesSchema(Schema):
    id = fields.Integer(dump_only=True)

    nome = fields.String(validate=validate.Length(max=128))
    descricao = fields.String(validate=validate.Length(max=128))

class Meta:
    unknown = EXCLUDE