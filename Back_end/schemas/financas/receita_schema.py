from marshmallow import Schema, fields, EXCLUDE, validate
from schemas.financas.tipo_receita_schema import TipoDespesaSchema
from schemas.financas.status_financas_schema import StatusFinancasSchema
from schemas.venda_estoque.venda_schema import VendaSchema

class ReceitaSchema(Schema):
    id = fields.Integer(dump_only=True)

    tipo_receita_id = fields.Integer(required=True)
    tipo_receita = fields.Nested(
        TipoDespesaSchema,
        attribute="tipo_receita",
        dump_only=True,
        only=("nome",)
    )

    status_financas_id = fields.Integer(required=True)
    status = fields.Nested(
        StatusFinancasSchema,
        attribute="status_financas",
        dump_only=True,
        only=("nome",)
    )

    venda_id = fields.Integer(allow_none=True)
    venda = fields.Nested(
        VendaSchema,
        attribute="venda",
        dump_only=True,
        only=("tipo", )
    )

    granja_id = fields.Integer(required=True, load_only=True)

    data = fields.Date(required=True)
    valor = fields.Decimal(
        required=True,
        as_string=True,
        places=2,
        validate=validate.Range(min=0)
    )
    descricao = fields.String(
        allow_none=True, 
        validate=validate.Length(max=256)
    )

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)