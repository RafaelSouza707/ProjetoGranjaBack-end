from marshmallow import Schema, fields, EXCLUDE, validate

class EscolaridadesSchema(Schema):
    id = fields.Integer(dump_only=True)

    funcionario_id = fields.Integer(required=True)

    nome = fields.String(required=True, validate=validate.Length(max=128))

class Meta:
    unknown = EXCLUDE