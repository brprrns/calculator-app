import json
import pytest
from app import lambda_handler


def call(params):
    return lambda_handler({"queryStringParameters": params}, None)


def test_add():
    r = call({"op": "add", "a": "2", "b": "3"})
    assert r["statusCode"] == 200
    assert json.loads(r["body"])["result"] == 5


def test_subtract_negative_result_ok():
    assert json.loads(call({"op": "subtract", "a": "3", "b": "10"})["body"])["result"] == -7


def test_multiply():
    assert json.loads(call({"op": "multiply", "a": "4", "b": "5"})["body"])["result"] == 20


@pytest.mark.parametrize("params", [
    None,
    {},
    {"op": "divide", "a": "1", "b": "2"},
    {"op": "add", "a": "0", "b": "1"},
    {"op": "add", "a": "-1", "b": "1"},
    {"op": "add", "a": "2.5", "b": "1"},
    {"op": "add", "a": "abc", "b": "1"},
    {"op": "add", "a": "1"},
    {"op": "add", "a": "1" * 30, "b": "1"},
])
def test_bad_input_returns_400(params):
    assert call(params)["statusCode"] == 400