import json
import os
from unittest.mock import patch
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import (
    APIGatewayProxyEventV2,
)
import pytest
from typing import Dict

from api_run_simulation.simulation.query.queries.query_configuration import (
    QueryConfiguration,
)


class MockLambdaContext(LambdaContext):
    def __init__(self):
        self._function_name = "test-fn"
        self._memory_limit_in_mb = 128
        self._invoked_function_arn = (
            "arn:aws:lambda:eu-west-1:12345678:function:test-fn"
        )
        self._aws_request_id = "52fdfc07-2182-154f-163f-5f0f9a621d72"


AUTH_TOKEN = "abc"


class MockAPIGatewayProxyEventV2(APIGatewayProxyEventV2):
    def __init__(
        self,
        body: str = "",
        http_method: str = "POST",
        pathParams: Dict[str, str] = {},
    ):
        self._data = {
            "body": body,
            "httpMethod": http_method,
            "pathParameters": pathParams,
            "headers": {"Authorization": f"Bearer {AUTH_TOKEN}"},
        }


@pytest.fixture
def lambda_context() -> LambdaContext:
    return MockLambdaContext()


SCM_API_ID = "1234"
SCM_API_REGION = "west"
SCM_API_STAGE = "123"
SCM_REPO = "test"


@pytest.fixture
def scm_envs():
    """Mocked SCM envs for influx."""
    os.environ["SCM_API_ID"] = SCM_API_ID
    os.environ["SCM_API_REGION"] = SCM_API_REGION
    os.environ["SCM_API_STAGE"] = SCM_API_STAGE
    os.environ["SCM_REPO"] = SCM_REPO


def test_handler_valid_input(lambda_context, scm_envs):
    with patch("api_run_simulation.run_simulation.run_simulation") as patched:
        user_input = {"location": {"lat": 123, "long": 321}, "fuel": {"amount": 300}}
        expected_response = {"hello": "world"}
        patched.return_value = expected_response

        from api_run_simulation.handler import lambda_handler

        response = lambda_handler(
            MockAPIGatewayProxyEventV2(
                http_method="POST",
                pathParams={},
                body=json.dumps(user_input),
            ),
            lambda_context,
        )
        assert response.get("statusCode") == 200
        assert response.get("body") == json.dumps(expected_response)
