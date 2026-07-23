from marshmallow import Schema, fields, validate, EXCLUDE
from schemas.venda_estoque.produto_schema import ProdutoSchema


class ItemVendaSchema(Schema):
    id = fields.Integer(dump_only=True)

    venda_id = fields.Integer(required=True)
    produto_id = fields.Integer(required=True)
    produto = fields.Nested(ProdutoSchema)

    quantidade = fields.Decimal(
        required=True,
        validate=validate.Range(min=0),
        as_string=True
    )

    subtotal = fields.Decimal(
        required=True,
        as_string=True
    )

    class Meta:
        unknown = EXCLUDE