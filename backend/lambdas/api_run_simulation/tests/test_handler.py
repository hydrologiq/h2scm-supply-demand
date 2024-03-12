import json
import os
from unittest.mock import patch
from simulation.business.inputs.fuel import Fuel
from simulation.business.inputs.location import Location
from simulation.business.user_input import BusinessInput
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import (
    APIGatewayProxyEventV2,
)
import pytest
from typing import Dict
from simulation.logic.logic_output import LogicOutput

from simulation.query.queries.query_configuration import (
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
        queryStringParams: Dict[str, str] = {},
    ):
        self._data = {
            "body": body,
            "httpMethod": http_method,
            "pathParameters": pathParams,
            "queryStringParameters": queryStringParams,
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


def test_handler_logic_output_transform(lambda_context, scm_envs):
    with patch("simulation.run_simulation.run_simulation") as patched:
        user_input = {"location": {"lat": 123, "long": 321}, "fuel": {"amount": 300}}
        expected_response = LogicOutput([], [], [], [])
        patched.return_value = expected_response

        from api_run_simulation.handler import lambda_handler

        response = lambda_handler(
            MockAPIGatewayProxyEventV2(
                http_method="POST",
                pathParams={"repo": SCM_REPO},
                queryStringParams={"debug": False, "instances": ["default", "abc"]},
                body=json.dumps(user_input),
            ),
            lambda_context,
        )
        assert response.get("statusCode") == 200
        expected_resp = json.loads(expected_response.dumps())
        del expected_resp["logistic"]
        del expected_resp["fuel"]
        del expected_resp["storageRental"]
        assert response.get("body") == json.dumps(expected_resp)
        patched.assert_called_once_with(
            BusinessInput(location=Location(lat=123, long=321), fuel=Fuel(amount=300)),
            QueryConfiguration(
                scm_api_id=SCM_API_ID,
                scm_api_region=SCM_API_REGION,
                scm_api_stage=SCM_API_STAGE,
                scm_repo=SCM_REPO,
                scm_access_token=AUTH_TOKEN,
            ),
            ["default", "abc"],
        )


def test_handler_logic_output_transform_debug(lambda_context, scm_envs):
    with patch("simulation.run_simulation.run_simulation") as patched:
        user_input = {"location": {"lat": 123, "long": 321}, "fuel": {"amount": 300}}
        expected_response = LogicOutput([], [], [], [])
        patched.return_value = expected_response

        from api_run_simulation.handler import lambda_handler

        response = lambda_handler(
            MockAPIGatewayProxyEventV2(
                http_method="POST",
                pathParams={"repo": SCM_REPO},
                queryStringParams={"debug": True, "instances": ["default", "abc"]},
                body=json.dumps(user_input),
            ),
            lambda_context,
        )
        assert response.get("statusCode") == 200
        assert response.get("body") == expected_response.dumps()


def test_handler_no_path_param(lambda_context, scm_envs):
    from api_run_simulation.handler import lambda_handler

    response = lambda_handler(
        MockAPIGatewayProxyEventV2(
            http_method="POST",
            pathParams={},
            body=json.dumps({}),
        ),
        lambda_context,
    )
    assert response.get("statusCode") == 400
    assert response.get("body") == "Path parameter not provided -- repo is missing"
