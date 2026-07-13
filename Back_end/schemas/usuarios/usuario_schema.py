from marshmallow import Schema, fields, validate, EXCLUDE

class UsuarioSchema(Schema):
    id = fields.Integer(dump_only=True)

    sexo_id = fields.Integer(required=False, allow_none=True)

    nome = fields.String(required=True, validate=validate.Length(max=128))
    cpf = fields.String(required=False, validate=validate.Length(max=11), allow_none=True)
    data_nascimento = fields.Date(required=False, allow_none=True)
    email = fields.String(validate=validate.Length(max=128)) 
    senha = fields.String(validate=validate.Length(max=256), load_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    ativo = fields.Boolean(required=True)

    class Meta:
        unknown = EXCLUDE