from marshmallow import Schema, fields, validate, EXCLUDE
from schemas.aviario.status_lote_frango_schema import StatusLoteFrangoSchema

class LoteFrangoSchema(Schema):
    id = fields.Integer(dump_only=True)
    
    status_lote_frango_id = fields.Integer(required=False, load_only=True)
    status = fields.Nested(
        StatusLoteFrangoSchema,
        attribute="status_lote_frango",
        load_only=True,
        only=("nome",)
    )

    granja_id = fields.Integer(required=True, load_only=True)

    identificacao = fields.String(required=True, validate=validate.Length(max=32))
    quantidade_inicial = fields.Integer(required=True, validate=validate.Range(min=0))
    data_alojamento = fields.Date(required=True)
    fornecedor = fields.String(required=False, validate=validate.Length(max=128))
    quantidade_atual = fields.Integer(required=True, validate=validate.Range(min=0))
    observacao = fields.String(required=False, validate=validate.Length(max=512))

    class Meta:
        unknown = EXCLUDE