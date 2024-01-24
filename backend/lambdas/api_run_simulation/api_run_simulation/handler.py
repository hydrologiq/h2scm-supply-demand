import json
import os
from api_run_simulation.simulation.business.user_input import BusinessInput
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import (
    event_source,
    APIGatewayProxyEventV2,
)
from api_run_simulation.simulation.query.queries.query_configuration import (
    QueryConfiguration,
)
from api_run_simulation.run_simulation import run_simulation


def build_response(code: int, body: str | object):
    return {
        "statusCode": code,
        "body": body if (body and isinstance(body, str)) else json.dumps(body),
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type,x-api-key",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST",
        },
    }


def build_error(name: str, message: str = "", status: int = 400):
    return build_response(status, f"{name} -- {message}")


@event_source(data_class=APIGatewayProxyEventV2)
def lambda_handler(event: APIGatewayProxyEventV2, context: LambdaContext):
    try:
        access_token = None
        if (
            "headers" in event
            and "Authorization" in event["headers"]
            and isinstance(event["headers"]["Authorization"], str)
        ):
            access_token = event["headers"]["Authorization"].replace("Bearer ", "")
        else:
            raise Exception("No access token provided")

        query_config = QueryConfiguration(
            scm_api_id=os.environ["SCM_API_ID"],
            scm_api_region=os.environ["SCM_API_REGION"],
            scm_api_stage=os.environ["SCM_API_STAGE"],
            scm_repo=os.environ["SCM_REPO"],
            scm_access_token=access_token,
        )

        return build_response(
            200,
            run_simulation(
                BusinessInput.from_dict(json.loads(event.body)), query_config
            ),
        )
    except Exception as ex:
        return build_error("Failed to run simulation", str(ex))
