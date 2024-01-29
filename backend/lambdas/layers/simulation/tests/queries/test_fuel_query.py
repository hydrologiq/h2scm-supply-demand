# import json
import json
import pytest
from simulation.query.queries import (
    QueryConfiguration,
    FuelQuery,
    FuelQueryInput,
)
from requests_mock import Mocker
from tests.data import SPARQL_QUERY_FUEL_RESPONSE, sparql_query_fuel

JSON_OUTPUT = json.loads(
    """
    {
      "fuel": [
        {
          "price": { "id": "hydrogen_nrmm:4", "monetaryValue": 40.0 },
          "service": { "id": "hydrogen_nrmm:3", "name": "Fuel Service 1" },
          "dispenser": { "id": "hydrogen_nrmm:31", "name": "Dispensing Site 1", "fillRate": 10, "fillingStationCapacity": 3, "lat": 123, "long": 43.2 },
          "producer": { "id": "hydrogen_nrmm:312", "name": "Hydrogen Producer 1", "dailyOfftakeCapacity": 600 }
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
    status_code: int = 200,
    repo: str = DEFAULT_REPO,
):
    return requests_mock.register_uri(
        "POST",
        f"https://{SCM_API_ID}.execute-api.{SCM_API_REGION}.amazonaws.com/{SCM_API_STAGE}/repositories/{repo}/query/select?graphs=default",
        request_headers={
            "Authorization": f"Bearer {MOCKED_ACCESS_TOKEN}",
        },
        status_code=status_code,
        additional_matcher=lambda request: request.text == query,
        json=response,
    )


def test_error_empty_response(requests_mock: Mocker):
    fuel_query = FuelQuery(
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

    fuel_total = 125

    register_sparql_query_mock(
        requests_mock,
        sparql_query_fuel(fuel_total),
        "",
    )

    with pytest.raises(Exception) as e_info:
        fuel_query.query(FuelQueryInput(fuel_total))
    assert str(e_info.value) == "failed to transform JSON from query"


def test_error_response(requests_mock: Mocker):
    fuel_query = FuelQuery(
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

    fuel_total = 125

    register_sparql_query_mock(
        requests_mock,
        sparql_query_fuel(fuel_total),
        "",
        400,
    )

    with pytest.raises(Exception) as e_info:
        fuel_query.query(FuelQueryInput(fuel_total))
    assert (
        str(e_info.value)
        == "400 Client Error: None for url: https://abcdef.execute-api.eu-west-2.amazonaws.com/dev/repositories/live/query/select?graphs=default"
    )


def test_run_fuel_query(requests_mock: Mocker):
    fuel_query = FuelQuery(
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

    fuel_total = 125

    register_sparql_query_mock(
        requests_mock,
        sparql_query_fuel(fuel_total),
        SPARQL_QUERY_FUEL_RESPONSE,
    )

    fuel_output = fuel_query.query(FuelQueryInput(fuel_total))

    assert requests_mock.last_request is not None
    assert len(fuel_output) == 1
    assert json.loads(fuel_output[0].dumps()) == JSON_OUTPUT["fuel"][0]
