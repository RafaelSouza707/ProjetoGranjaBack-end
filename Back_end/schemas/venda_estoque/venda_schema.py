from marshmallow import Schema, fields, validate, EXCLUDE
from schemas.usuarios.cliente_schema import ClienteSchema
from schemas.venda_estoque.status_venda_schema import StatusVendaSchema
from schemas.financas.status_financas_schema import StatusFinancasSchema

class VendaSchema(Schema):
    id = fields.Integer(dump_only=True)

    cliente_id = fields.Integer(required=False, allow_none=True)
    cliente = fields.Nested(
        ClienteSchema,
        attribute="cliente",
        dump_only=True,
        only=("id", "nome")
    )

    status_financas_id = fields.Integer(required=True)
    status = fields.Nested(
        StatusFinancasSchema,
        attribute="status_financas",
        dump_only=True
    )

    tipo_venda_id = fields.Integer(required=True)
    tipo = fields.Nested(
        StatusVendaSchema,
        attribute="status_venda",
        dump_only=True
    )

    granja_id = fields.Integer(
        required=True
    )

    valor_total = fields.Decimal(required=True, as_string=True, places=2, validate=validate.Range(min=0))
    data_venda = fields.Date(required=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        unknown = EXCLUDE