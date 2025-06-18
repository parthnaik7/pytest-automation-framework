from jsonschema import validate, ValidationError

def validate_schema(response_json, schema):
    try:
        validate(instance=response_json, schema=schema)
        return True
    except ValidationError as e:
        print(f"Schema validation error: {e}")
        return False