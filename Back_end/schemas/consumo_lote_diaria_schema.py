from marshmallow import Schema, fields, validate

from schemas.lote_frango_schema import LoteFrangoSchema

class ConsumoLoteDiariaSchema(Schema):
    id = fields.Integer(dump_only=True)

    id_lote_frango = fields.Integer(required=True)

    id_lote_racao = fields.Integer(required=True)
    
    data = fields.Date(required=True)
    
    quilos = fields.Decimal(required=True, as_string=True, places=3, validate=validate.Range(min=0))