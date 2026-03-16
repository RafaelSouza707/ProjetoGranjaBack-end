from marshmallow import Schema, fields


from schemas.lote_frango_schema import LoteFrangoSchema

class MortalidadeSchema(Schema):
    id = fields.Integer(dump_only=True)

    id_lote_frango = fields.Integer(required=True)
    data = fields.Date(required=True)
    quantidade_mortes = fields.Integer(required=True)

    lote_frango = fields.Nested(LoteFrangoSchema(only=("id", "fornecedor", "tipo_lote", "galpao")), dump_only=True)