from marshmallow import Schema, fields, validate, EXCLUDE
from decimal import Decimal

class ConsumoLoteDiariaSchema(Schema):
    id = fields.Integer(dump_only=True)

    lote_frango_id = fields.Integer(required=True)
    lote_racao_id = fields.Integer(required=True)
    
    data = fields.Date(required=True)
    quilos = fields.Decimal(
        required=True, 
        as_string=True, 
        places=3, 
        validate=validate.Range(min=Decimal(0))
    )

    class Meta:
        unknown = EXCLUDE