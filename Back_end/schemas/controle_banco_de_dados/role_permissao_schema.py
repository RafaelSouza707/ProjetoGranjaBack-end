from marshmallow import Schema, fields, EXCLUDE

class RolePermissaoSchema(Schema):
    id = fields.Integer(dump_only=True)

    role_id = fields.Integer(required=True)
    permissao_id = fields.Integer(required=True)

class Meta:
    unknown = EXCLUDE