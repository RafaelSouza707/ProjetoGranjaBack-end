from marshmallow import Schema, fields, validate, EXCLUDE
from schemas.aviario.tipo_produto_schema import TipoProdutoSchema
from schemas.venda_estoque.tipo_unidade_medida_schema import TipoUnidadeMedidaSchema

class ProdutoSchema(Schema):
    id = fields.Integer(dump_only=True)

    tipo_produto_id = fields.Integer(required=True)
    tipo_produto = fields.Nested(
        TipoProdutoSchema,
        attribute="tipo_produto",
        only=("nome",)
    )

    tipo_unidade_medida_id = fields.Integer(required=True)
    tipo_unidade_medida = fields.Nested(
        TipoUnidadeMedidaSchema,
        attribute="tipo_unidade_medida",
        only=("sigla", "id")
    )

    granja_id = fields.Integer(required=True, load_only=True)

    descricao = fields.String(validate=validate.Length(max=128), required=False, allow_none=True)
    quantidade_estoque = fields.Decimal(places=3, validate=validate.Range(min=0), as_string=True)
    ativo = fields.Boolean()
    data_cadastro = fields.Date(required=True)


    class Meta:
        unknown = EXCLUDE