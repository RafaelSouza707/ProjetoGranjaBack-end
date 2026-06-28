from marshmallow import Schema, fields, EXCLUDE, validate

class GranjaSchema(Schema):

    id = fields.Integer(dump_only=True)

    identificacao = fields.String(required=True, validate=validate.Length(max=32))

    created_at = fields.DateTime(dump_only=True)

    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        unknown = EXCLUDE