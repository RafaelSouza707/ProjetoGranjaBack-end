from marshmallow import Schema, fields, validate, EXCLUDE

class CleinteSchema(Schema):
    id = fields.Integer(dump_only=True)

    tipo = fields.String(
        required=True,
        validate=validate.OneOf(["PF", "PJ"])
    )

    documento = fields.String(required=True)

    telefone = fields.String(validate=validate.Length(min=1, max=20))
    email = fields.String(validate=validate.Length(min=1, max=128))

class Meta:
    unknown = EXCLUDE