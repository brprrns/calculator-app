import json

from calculator.handler import lambda_handler


def call(query=None, body=None):
    event = {"queryStringParameters": query, "body": json.dumps(body) if body is not None else None}
    response = lambda_handler(event, None)
    return response["statusCode"], json.loads(response["body"])


def test_get_add():
    status, body = call(query={"operation": "add", "a": "10", "b": "5"})
    assert status == 200
    assert body["result"] == 15


def test_post_multiply():
    status, body = call(body={"operation": "multiply", "a": 6, "b": 7})
    assert status == 200
    assert body["result"] == 42


def test_subtract_negative_result_is_fine():
    status, body = call(query={"operation": "subtract", "a": "2", "b": "5"})
    assert status == 200
    assert body["result"] == -3


def test_operation_is_case_insensitive():
    status, body = call(query={"operation": "ADD", "a": "1", "b": "2"})
    assert status == 200
    assert body["result"] == 3


def test_unknown_operation():
    status, body = call(query={"operation": "divide", "a": "4", "b": "2"})
    assert status == 400
    assert "operation" in body["error"]


def test_missing_parameter():
    status, body = call(query={"operation": "add", "a": "4"})
    assert status == 400
    assert "b" in body["error"]


def test_no_parameters_at_all():
    status, _ = call()
    assert status == 400


def test_negative_number_rejected():
    status, _ = call(query={"operation": "add", "a": "-4", "b": "2"})
    assert status == 400


def test_decimal_rejected():
    status, _ = call(query={"operation": "add", "a": "2.5", "b": "2"})
    assert status == 400


def test_text_rejected():
    status, _ = call(query={"operation": "add", "a": "abc", "b": "2"})
    assert status == 400


def test_bad_json_body():
    event = {"queryStringParameters": None, "body": "{not json"}
    response = lambda_handler(event, None)
    assert response["statusCode"] == 400
