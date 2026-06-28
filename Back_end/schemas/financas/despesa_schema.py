from marshmallow import Schema, fields, EXCLUDE, validate
from schemas.financas.tipo_despesa_schema import TipoDespesaSchema
from schemas.financas.status_financas_schema import StatusFinancasSchema
from schemas.aviario.lote_frango_schema import LoteFrangoSchema

class DespesaSchema(Schema):
    id = fields.Integer(dump_only=True)

    tipo_despesa_id = fields.Integer(required=True)
    tipo = fields.Nested(
        TipoDespesaSchema,
        attribute="tipo_despesa",
        dump_only=True
    )

    status_financas_id = fields.Integer(required=True)
    status = fields.Nested(
        StatusFinancasSchema,
        attribute="status_financas",
        dump_only=True
    )
    
    lote_frango_id = fields.Integer(allow_none=True)
    lote_frango = fields.Nested(
        LoteFrangoSchema,
        attribute="lote_frango",
        dump_only=True,
        only=("id", "identificacao")
    )

    granja_id = fields.Integer(required=True, load_only=True)

    data = fields.Date(required=True)
    data_vencimento = fields.Date(allow_none=True)

    valor = fields.Decimal( 
        required=True,
        as_string=True,
        places=2,
        validate=validate.Range(min=0)
    )

    descricao = fields.String(allow_none=True, validate=validate.Length(max=256))

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        unknown = EXCLUDE