from marshmallow import Schema, fields, validate, EXCLUDE

class ContaADMSchema(Schema):
    id = fields.Integer(dump_only=True)

    role_id = fields.Integer(required=True)

    nome = fields.String(required=True, validate=validate.Length(min=1, max=128))
    email = fields.String(required=True, validate=validate.Length(min=1, max=128))
    senha = fields.String(required=True, validate=validate.Length(min=1, max=256))
    cpf = fields.String(required=True, validate=validate.Length(min=11, max=11))
    data_cadastro = fields.Date(required=True)

class Meta:
    unknown = EXCLUDE