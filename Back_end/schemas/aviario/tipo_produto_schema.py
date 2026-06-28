from marshmallow import Schema, fields, validate, EXCLUDE

class TipoProdutoSchema(Schema):
    id = fields.Integer(dump_only=True)

    granja_id = fields.Integer(required=True, load_only=True)

    nome = fields.String(required=True, validate=validate.Length(max=64))

    class Meta:
        unknown = EXCLUDE