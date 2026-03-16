from marshmallow import Schema, fields
from schemas.lote_frango_schema import LoteFrangoSchema


class CorteSchema(Schema):
    id = fields.Integer(dump_only=True)

    id_lote_frango = fields.Integer(required=True)

    data = fields.Date(required=True)

    peso = fields.Decimal(required=True, as_string=True, places=3)

    lote_frango = fields.Nested(LoteFrangoSchema(only=("id", "fornecedor", "tipo_lote", "galpao")), dump_only=True)