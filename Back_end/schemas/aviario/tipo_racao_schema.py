from marshmallow import Schema, fields, validate, EXCLUDE

class TipoRacaoSchema(Schema):

    id = fields.Integer(dump_default=True)

    granja_id = fields.Integer(required=True, load_only=True)

    nome = fields.String(required=True, validate=validate.Length(max=64))
    descricao = fields.String(required=False, validate=validate.Length(max=256), allow_none=True)

    class Meta:
        unknown = EXCLUDE