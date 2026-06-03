from marshmallow import Schema, fields, validate, EXCLUDE
from decimal import Decimal

class ProducaoSchema(Schema):
    id = fields.Integer(dump_only=True)

    lote_frango_id = fields.Integer(required=True)
    produto_id = fields.Integer(required=True)

    quantidade = fields.Decimal(required=True, validate=validate.Range(min=Decimal(0)))
    data_producao = fields.Date(required=True)
    observacao = fields.String(validate=validate.Length(max=512))

class Meta:
    unknown = EXCLUDE