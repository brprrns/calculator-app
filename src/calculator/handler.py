"""AWS Lambda entry point (sits behind API Gateway).

Two ways to call it:
    GET  /calculate?operation=add&a=10&b=5
    POST /calculate   with body {"operation": "add", "a": 10, "b": 5}
"""
import json
import re

from calculator.operations import add, subtract, multiply

OPERATIONS = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
}

# query string values always arrive as text, so only plain digits get converted
_DIGITS_ONLY = re.compile(r"[0-9]+")


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def _read_params(event):
    params = {}
    params.update(event.get("queryStringParameters") or {})

    raw_body = event.get("body")
    if raw_body:
        try:
            data = json.loads(raw_body)
        except json.JSONDecodeError:
            raise ValueError("Request body is not valid JSON")
        if not isinstance(data, dict):
            raise ValueError("Request body must be a JSON object")
        params.update(data)
    return params


def _get_number(params, name):
    if name not in params:
        raise ValueError(f"Missing parameter: {name}")
    value = params[name]
    if isinstance(value, str) and _DIGITS_ONLY.fullmatch(value):
        return int(value)
    return value  # anything else gets rejected by the validation in operations.py


def lambda_handler(event, context):
    try:
        params = _read_params(event)

        operation = str(params.get("operation", "")).lower()
        if operation not in OPERATIONS:
            supported = ", ".join(OPERATIONS)
            raise ValueError(f"operation must be one of: {supported}")

        a = _get_number(params, "a")
        b = _get_number(params, "b")
        result = OPERATIONS[operation](a, b)
    except ValueError as err:
        return _response(400, {"error": str(err)})

    return _response(200, {"operation": operation, "a": a, "b": b, "result": result})
