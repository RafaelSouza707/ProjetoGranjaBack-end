from marshmallow import Schema, fields, validate, EXCLUDE
from decimal import Decimal

class MovimentacaoEstoqueSchema(Schema):
    id = fields.Integer(dump_only=True)

    produto_id = fields.Integer(required=True)
    producao_id = fields.Integer(required=True)
    item_venda_id = fields.Integer(required=True)
    tipo_movimentacao_id = fields.Integer(required=True)

    quantidade = fields.Decimal(required=True, validate=validate.Range(min=0))
    updated_at = fields.DateTime(required=True)
    observacao = fields.String(required=True, validate=validate.Length(max=256))

    class Meta:
        unknown = EXCLUDE