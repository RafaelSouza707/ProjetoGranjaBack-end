from marshmallow import Schema, fields, validate, EXCLUDE

class RoleSchema(Schema):
    id = fields.Integer(dump_only=True)

    nome = fields.String(validate=validate.Length(max=128))

class Meta:
    unknown = EXCLUDE