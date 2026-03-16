from marshmallow import Schema, fields, validate


class LoteRacaoSchema(Schema):
    id = fields.Integer(dump_only=True)

    tipo_racao = fields.String(required=True, validate=validate.Length(max=30))

    fornecedor = fields.String(required=True, validate=validate.Length(max=100))

    data_compra = fields.Date(required=True)

    quilos = fields.Decimal(required=True, as_string=True, places=3)

    valor = fields.Decimal(required=True, as_string=True, places=2)

    