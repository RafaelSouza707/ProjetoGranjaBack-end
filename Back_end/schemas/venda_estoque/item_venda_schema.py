from marshmallow import Schema, fields, validate, EXCLUDE
from decimal import Decimal

class ItemVendaSchema(Schema):
    id = fields.Integer(dump_only=True)

    venda_id = fields.Integer(required=True)
    produto_id = fields.Integer(required=True)

    quantidade = fields.Decimal(required=True, validate=validate.Range(min=0))

    class Meta:
        unknown = EXCLUDE