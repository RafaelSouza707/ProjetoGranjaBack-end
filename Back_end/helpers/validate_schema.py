from marshmallow import ValidationError

def validate_schema(schema, json_data, partial=False):
    if json_data is None:
        return None, {"erro": "Dados não fornecidos"}

    try:
        data = schema.load(json_data, partial=partial)
        return data, None

    except ValidationError as err:
        return None, err.messages