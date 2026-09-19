import json
from calculator import add, subtract, multiply

OPERATIONS = {"add": add, "subtract": subtract, "multiply": multiply}
MAX_DIGITS = 15


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def _parse(value, name):
    if value is None or str(value).strip() == "":
        raise ValueError(f"Query parameter '{name}' is required")
    text = str(value).strip()
    if not (text.isascii() and text.isdigit()):
        raise ValueError(f"'{name}' must be a positive whole number")
    if len(text) > MAX_DIGITS:
        raise ValueError(f"'{name}' is too large (max {MAX_DIGITS} digits)")
    number = int(text)
    if number <= 0:
        raise ValueError(f"'{name}' must be greater than 0")
    return number


def lambda_handler(event, context):
    params = (event or {}).get("queryStringParameters") or {}
    op = str(params.get("op") or "").lower()
    if op not in OPERATIONS:
        return _response(400, {"error": "op must be one of: add, subtract, multiply"})
    try:
        a = _parse(params.get("a"), "a")
        b = _parse(params.get("b"), "b")
    except ValueError as exc:
        return _response(400, {"error": str(exc)})
    result = OPERATIONS[op](a, b)
    return _response(200, {"operation": op, "a": a, "b": b, "result": result})