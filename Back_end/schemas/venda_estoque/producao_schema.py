from marshmallow import Schema, fields, validate, EXCLUDE
from decimal import Decimal
from schemas.aviario.lote_frango_schema import LoteFrangoSchema
from schemas.venda_estoque.produto_schema import ProdutoSchema

class ProducaoSchema(Schema):
    id = fields.Integer(dump_only=True)

    lote_frango_id = fields.Integer(required=True)
    lote_frango = fields.Nested(
        LoteFrangoSchema,
        attribute="lote_frango",
        only=("identificacao", )
    )
    
    produto_id = fields.Integer(required=True)
    produto = fields.Nested(
        ProdutoSchema,
        attribute=("produto"),
        only=("tipo_produto", "tipo_unidade_medida")
    )

    quantidade = fields.Decimal(required=True, validate=validate.Range(min=0), as_string=True)
    data_producao = fields.Date(required=True)
    observacao = fields.String(validate=validate.Length(max=512), required=False, allow_none=True)

    class Meta:
        unknown = EXCLUDE