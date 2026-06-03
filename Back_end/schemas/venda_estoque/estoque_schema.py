from marshmallow import Schema, fields, validate, EXCLUDE
from decimal import Decimal

class EstoqueSchema(Schema):
    id = fields.Integer(dump_only=True)

    produto_id = fields.Integer(required=True)

    quantidade_atual = fields.Decimal(validate=validate.Range(min=Decimal(0)))
    updated_at = fields.DateTime(required=True)

class Meta:
    unknown = EXCLUDE