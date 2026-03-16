from marshmallow import Schema, fields, validate

class LoteFrangoSchema(Schema):
    id = fields.Integer(dump_only=True)

    quantidade_inicial = fields.Integer(required=True)

    data_entrada_aves = fields.Date(required=True)

    data_ninhada = fields.Date()

    fornecedor = fields.String(validate=validate.Length(max=100))

    tipo_lote = fields.String(validate=validate.Length(max=20))

    galpao = fields.Integer()

    status = fields.String(validate=validate.Length(max=50))
    
    peso_medio = fields.Decimal(as_string=True)