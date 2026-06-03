from marshmallow import Schema, fields, validate, EXCLUDE

class LoteFrangoSchema(Schema):
    id = fields.Integer(dump_only=True)
    
    status_lote_frango_id = fields.Integer(required=True)

    identificacao = fields.String(required=True, validate=validate.Length(64))
    quantidade_inicial = fields.Integer(required=True, validate=validate.Range(min=0))
    data_alojamento = fields.Date(required=True)
    fornecedor = fields.String(validate=validate.Length(max=128))
    quantidade_atual = fields.Integer(required=True, validate=validate.Range(min=0))
    observação = fields.String(validate=validate.Length(max=512))

class Meta:
    unknown = EXCLUDE