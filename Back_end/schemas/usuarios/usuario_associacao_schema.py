from marshmallow import Schema, fields, EXCLUDE
from schemas.usuarios.usuario_schema import UsuarioSchema

class UsuarioAssociacaoSchema(Schema):
    id = fields.Integer(dump_only=True)

    usuario_origem_id = fields.Integer(required=True)

    usuario_destino_id = fields.Integer(required=True)
    usuario_destino = fields.Nested(
        UsuarioSchema,
        dump_only=True,
        only=("nome", "email")
    )

    status = fields.String()

    class Meta:
        unknown = EXCLUDE