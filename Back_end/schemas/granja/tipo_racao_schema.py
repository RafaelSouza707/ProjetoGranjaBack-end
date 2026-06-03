from marshmallow import Schema, fields, validate, EXCLUDE

class TipoRacaoSchema(Schema):

    id = fields.Integer(dump_default=True)

    nome = fields.String(required=True, validate=validate.Length(64))
    descricao = fields.String(required=True, validate=validate.Length(max=256))

class Meta:
    unknown = EXCLUDE