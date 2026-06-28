from marshmallow import Schema, fields, EXCLUDE, validate


class UsuarioGranjaSchema(Schema):

    id = fields.Integer(dump_only=True)

    usuario_id = fields.Integer(required=True)

    granja_id = fields.Integer(required=True)

    cargo_id = fields.Integer(required=True)

    ativo = fields.Boolean(required=True)

    class Meta:
        unknown = EXCLUDE