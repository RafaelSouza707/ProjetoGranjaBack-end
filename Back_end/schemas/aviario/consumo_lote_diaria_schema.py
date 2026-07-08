from marshmallow import Schema, fields, validate, EXCLUDE
from decimal import Decimal
from schemas.aviario.lote_frango_schema import LoteFrangoSchema
from schemas.aviario.lote_racao_schema import LoteRacaoSchema

class ConsumoLoteDiariaSchema(Schema):
    id = fields.Integer(dump_only=True)

    lote_frango_id = fields.Integer(required=True)

    lote_racao_id = fields.Integer(required=True)
    lote_racao = fields.Nested(
        LoteRacaoSchema,
        attribute="lote_racao",
        only=("tipo_racao.nome", "tipo_racao.id")
    )
    
    data = fields.Date(required=True)
    quilos = fields.Decimal(
        required=True, 
        as_string=True, 
        places=3, 
        validate=validate.Range(min=Decimal(0))
    )

    class Meta:
        unknown = EXCLUDE