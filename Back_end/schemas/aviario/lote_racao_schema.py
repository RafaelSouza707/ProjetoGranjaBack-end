from marshmallow import Schema, fields, validate, EXCLUDE
from schemas.aviario.tipo_racao_schema import TipoRacaoSchema

class LoteRacaoSchema(Schema):
    id = fields.Integer(dump_only=True)

    tipo_racao_id = fields.Integer(required=True, load_only=True)
    tipo_racao = fields.Nested(
        TipoRacaoSchema,
        attribute="tipo_racao",
        dump_only=True
    )

    granja_id = fields.Integer(required=True, load_only=True)

    fornecedor = fields.String(required=True, validate=validate.Length(max=128))
    data_compra = fields.Date(required=True)
    quilos = fields.Decimal(required=True, as_string=True, places=3, validate=validate.Range(min=0))
    

    class Meta:
        unknown = EXCLUDE