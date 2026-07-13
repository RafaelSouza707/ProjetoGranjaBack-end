from marshmallow import Schema, fields, validate, EXCLUDE

class TipoVendaSchema(Schema):
    id = fields.Integer(dump_only=True)

    granja_id = fields.Integer(required=True, load_only=True)

    nome = fields.String(required=True, validate=validate.Length(max=32))

    class Meta:
        unknown = EXCLUDE