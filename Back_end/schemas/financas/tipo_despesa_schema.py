from marshmallow import Schema, fields, validate, EXCLUDE

class TipoDespesaSchema(Schema):
    id = fields.Integer(dump_only=True)

    nome = fields.String(
        required=True, 
        validate=validate.Length(max=128)
    )


class Meta:
    unknown = EXCLUDE