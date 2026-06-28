from marshmallow import Schema, fields, validate, EXCLUDE

class TipoMovimentacaoSchema(Schema):
    id = fields.Integer(dump_only=True)

    granja_id = fields.Integer(
        required=True
    )

    usuario = fields.Integer(required=True, load_only=True)

    sigla = fields.String(required=True, validate=validate.Length(max=8))
    descricao = fields.String(required=True, validate=validate.Length(max=64))

    class Meta:
        unknown = EXCLUDE