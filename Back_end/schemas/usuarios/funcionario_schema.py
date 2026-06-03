from marshmallow import Schema, fields, validate, EXCLUDE

class FuncionarioSchema(Schema):
    id = fields.Integer(dump_only=True)

    cargo_id = fields.Integer(required=True)
    sexo_id = fields.Integer(required=True)

    nome = fields.String(required=True, validate=validate.Length(max=128))
    cpf = fields.String(required=True, validate=validate.Length(max=11))
    data_nascimento = fields.Date()
    email = fields.String(validate=validate.Length(max=128)) 
    senha = fields.String(validate=validate.Length(max=256))
    data_entrada = fields.Date()
    salario = fields.Decimal(as_string=True, places=2)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    ativo = fields.Boolean(required=True)

class Meta:
    unknown = EXCLUDE