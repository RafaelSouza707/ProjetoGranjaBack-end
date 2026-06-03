from marshmallow import Schema, fields, validate, EXCLUDE

class EnderecoSchema(Schema):
    id = fields.Integer(dump_only=True)

    usuario_id = fields.Integer(required=True)

    cep = fields.String(validate=validate.Length(max=8))
    rua = fields.String(validate=validate.Length(max=128))
    numero = fields.String(validate=validate.Length(max=10))
    bairro_logradouro = fields.String(validate=validate.Length(128))
    cidade = fields.String(validate=validate.Length(128))

class Meta:
    unknown = EXCLUDE