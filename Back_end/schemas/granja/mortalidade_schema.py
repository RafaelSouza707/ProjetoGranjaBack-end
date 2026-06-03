from marshmallow import Schema, fields, validate, EXCLUDE

class MortalidadeSchema(Schema):
    id = fields.Integer(dump_only=True)

    lote_frango_id = fields.Integer(required=True)

    data = fields.Date(required=True)
    quantidade_mortes = fields.Integer(required=True, validate=validate.Range(min=1))


class Meta:
    unknown = EXCLUDE