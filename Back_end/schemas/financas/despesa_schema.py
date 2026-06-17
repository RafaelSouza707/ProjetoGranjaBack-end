from marshmallow import Schema, fields, EXCLUDE, validate

class DespesaSchema(Schema):
    id = fields.Integer(dump_only=True)

    tipo_despesa_id = fields.Integer(required=True)
    status_financas_id = fields.Integer(required=True)
    lote_frango_id = fields.Integer(allow_none=True)

    data = fields.Date(required=True)
    data_vencimento = fields.Date(allow_none=True)

    valor = fields.Decimal(
        required=True,
        as_string=True,
        places=2
    )

    descricao = fields.String(validate=validate.Length(max=256))

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        unknown = EXCLUDE