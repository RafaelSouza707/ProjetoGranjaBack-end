from marshmallow import Schema, fields, validate, EXCLUDE

class ClienteSchema(Schema):
    id = fields.Integer(dump_only=True)

    granja_id = fields.Integer(required=True, load_only=True)

    nome = fields.String(required=True, validate=validate.Length(max=128))
    
    documento = fields.String(required=False, allow_none=True)

    telefone = fields.String(validate=validate.Length(min=1, max=32), allow_none=True)
    email = fields.String(validate=validate.Length(min=1, max=128), allow_none=True)

    class Meta:
        unknown = EXCLUDE