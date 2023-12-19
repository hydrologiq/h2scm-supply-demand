import json
from simulation.query.queries import (
    QueryConfiguration,
    LogisticQuery,
    LogisticQueryInput,
)
from requests_mock import Mocker
from tests.simulation.data import SPARQL_QUERY_LOGISTIC_RESPONSE, sparql_query_logistic

JSON_INPUT = json.loads(
    """
    {
        "fuel": [
            {
                "type": "TubeTrailer",
                "amount": 300
            },
            {
                "type": "TubeTrailer",
                "amount": 185
            }
        ],
        "project": {
            "location": {
                "lat": 12.234,
                "long": 43.221   
            }
        }
    }
    """
)

JSON_OUTPUT = json.loads(
    """
    {
      "logistic": [
        {
          "service": { "id": "hydrogen_nrmm:1", "name": "Service 1" },
          "storage": { "id": "hydrogen_nrmm:12", "name": "Tube Trailer 1", "capacity": 300, "availableQuantity": 3 },
          "vehicle": { "id": "hydrogen_nrmm:123", "name": "Vehicle 1", "availableQuantity": 1, "transportDistance": 123 },
          "projectDistance": 12.345
        },
        {
          "service": { "id": "hydrogen_nrmm:2", "name": "Service 2" },
          "storage": { "id": "hydrogen_nrmm:21", "name": "Tube Trailer 2", "capacity": 225, "availableQuantity": 1 },
          "vehicle": { "id": "hydrogen_nrmm:212", "name": "Vehicle 2", "availableQuantity": 2, "transportDistance": 123 },
          "projectDistance": 54.321
        }
      ]
    }
    """
)

SCM_API_ID = "abcdef"
SCM_API_REGION = "eu-west-2"
SCM_API_STAGE = "dev"

DEFAULT_REPO = "live"
MOCKED_ACCESS_TOKEN = "abcdefgtoken"


def register_sparql_query_mock(
    requests_mock: Mocker,
    query: str,
    response: str | object,
    repo: str = DEFAULT_REPO,
):
    return requests_mock.register_uri(
        "POST",
        f"https://{SCM_API_ID}.execute-api.{SCM_API_REGION}.amazonaws.com/{SCM_API_STAGE}/repositories/{repo}/query/select",
        request_headers={
            "Authorization": f"Bearer {MOCKED_ACCESS_TOKEN}",
        },
        status_code=200,
        additional_matcher=lambda request: request.text == query,
        json=response,
    )


def test_run_logistic_query(requests_mock: Mocker):
    logistic_query = LogisticQuery(
        QueryConfiguration(
            **{
                "scm_api_id": SCM_API_ID,
                "scm_api_region": SCM_API_REGION,
                "scm_api_stage": SCM_API_STAGE,
                "scm_repo": DEFAULT_REPO,
                "scm_access_token": MOCKED_ACCESS_TOKEN,
            }
        )
    )

    minStorage = 125
    lat = 12.55
    long = 12.66

    register_sparql_query_mock(
        requests_mock,
        sparql_query_logistic(minStorage, lat, long),
        SPARQL_QUERY_LOGISTIC_RESPONSE,
    )

    logistic_output = logistic_query.query(LogisticQueryInput(minStorage, lat, long))

    assert requests_mock.last_request is not None
    assert len(logistic_output) == 2
    assert json.loads(logistic_output[0].dumps()) == JSON_OUTPUT["logistic"][0]
    assert json.loads(logistic_output[1].dumps()) == JSON_OUTPUT["logistic"][1]
