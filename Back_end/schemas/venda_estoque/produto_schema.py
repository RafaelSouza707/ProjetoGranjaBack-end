from marshmallow import Schema, fields, validate, EXCLUDE

class ProdutoSchema(Schema):
    id = fields.Integer(dump_only=True)

    tipo_produto_id = fields.Integer(required=True)
    tipo_unidade_medida_id = fields.Integer(required=True)

    descricao = fields.String(validate=validate.Length(max=128))
    quantidade_estoque = fields.Decimal(places=3)
    ativo = fields.Boolean()
    data_cadastro = fields.Date(required=True)


class Meta:
    unknown = EXCLUDE