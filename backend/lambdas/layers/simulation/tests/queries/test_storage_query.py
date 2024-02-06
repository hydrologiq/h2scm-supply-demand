import copy
import json
from simulation.query.queries import (
    QueryConfiguration,
    StorageQuery,
    StorageQueryInput,
)
from requests_mock import Mocker
from tests.helpers.storage import (
    StorageResponse,
    storage_query_response_json,
    sparql_query_storage,
)
import simulation.business.outputs as BusinessOutputs

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
      "storageRental": [
        {
          "company": { "id": "hydrogen_nrmm:15" },
          "service": { "id": "hydrogen_nrmm:1", "name": "Service 1" },
          "storage": { "id": "hydrogen_nrmm:12", "name": "Tube Trailer 1", "capacity": 300, "availableQuantity": 3 },
          "quote": { "id": "hydrogen_nrmm:12345", "monetaryValuePerUnit": 80 }
        },
        {
          "company": { "id": "hydrogen_nrmm:25" },
          "service": { "id": "hydrogen_nrmm:2", "name": "Service 2" },
          "storage": { "id": "hydrogen_nrmm:21", "name": "Tube Trailer 2", "capacity": 225, "availableQuantity": 1 },
          "quote": { "id": "hydrogen_nrmm:214", "monetaryValuePerUnit": 40 }
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
        f"https://{SCM_API_ID}.execute-api.{SCM_API_REGION}.amazonaws.com/{SCM_API_STAGE}/repositories/{repo}/query/select?graphs=default",
        request_headers={
            "Authorization": f"Bearer {MOCKED_ACCESS_TOKEN}",
        },
        status_code=200,
        additional_matcher=lambda request: request.text == query,
        json=response,
    )


LOGISTIC_RESPONSE_1 = StorageResponse(
    storage="12",
    storageName="Tube Trailer 1",
    storageAvailableQuantity=3,
    storageCapacity=300,
    service="1",
    serviceName="Service 1",
    quote="12345",
    quoteMonetaryValuePerUnit=80.0,
    company="15",
)

LOGISTIC_RESPONSE_2 = StorageResponse(
    storage="21",
    storageName="Tube Trailer 2",
    storageAvailableQuantity=1,
    storageCapacity=225,
    service="2",
    serviceName="Service 2",
    quote="214",
    quoteMonetaryValuePerUnit=40.0,
    company="25",
)


def test_run_storage_query(requests_mock: Mocker):
    storage_query = StorageQuery(
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

    totalFuel = 125

    register_sparql_query_mock(
        requests_mock,
        sparql_query_storage(totalFuel),
        storage_query_response_json([LOGISTIC_RESPONSE_1, LOGISTIC_RESPONSE_2]),
    )

    storage_output = storage_query.query(StorageQueryInput(totalFuel))

    assert requests_mock.last_request is not None
    assert len(storage_output) == 2
    assert json.loads(storage_output[0].dumps()) == JSON_OUTPUT["storageRental"][0]
    assert json.loads(storage_output[1].dumps()) == JSON_OUTPUT["storageRental"][1]


LOGISTIC_RESPONSE_MCP = StorageResponse(
    storage="12",
    storageName="MCP Option 1",
    storageAvailableQuantity=12,
    storageCapacity=16.0,
    service="1",
    serviceName="Service 1",
    quote="12345",
    quoteMonetaryValuePerUnit=80.0,
    company="15",
)

JSON_OUTPUT_MCP = json.loads(
    """
    {
      "storageRental": [
        {
          "company": { "id": "hydrogen_nrmm:15" },
          "service": { "id": "hydrogen_nrmm:1", "name": "Service 1" },
          "storage": { "id": "hydrogen_nrmm:12", "name": "MCP Option 1", "capacity": 16, "availableQuantity": 12 },
          "quote": { "id": "hydrogen_nrmm:12345", "monetaryValuePerUnit": 80 }
        }
      ]
    }
    """
)


def test_run_storage_query_with_mcp(requests_mock: Mocker):
    storage_query = StorageQuery(
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

    totalFuel = 125

    register_sparql_query_mock(
        requests_mock,
        sparql_query_storage(totalFuel),
        storage_query_response_json([LOGISTIC_RESPONSE_MCP]),
    )

    storage_output = storage_query.query(StorageQueryInput(totalFuel))

    assert requests_mock.last_request is not None
    assert len(storage_output) == 1
    assert json.loads(storage_output[0].dumps()) == JSON_OUTPUT_MCP["storageRental"][0]


LOGISTIC_RESPONSE_2_DEPS = StorageResponse(
    storage="21",
    storageName="Tube Trailer 2",
    storageAvailableQuantity=1,
    storageCapacity=225,
    service="2",
    serviceName="Service 2",
    quote="214",
    quoteMonetaryValuePerUnit=40.0,
    company="25",
    serviceExclusiveUpstreamCompanies="5",
    serviceExclusiveDownstreamCompanies="6",
)


def test_run_storage_query_with_deps(requests_mock: Mocker):
    storage_query = StorageQuery(
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

    totalFuel = 125

    register_sparql_query_mock(
        requests_mock,
        sparql_query_storage(totalFuel),
        storage_query_response_json([LOGISTIC_RESPONSE_2_DEPS]),
    )

    storage_output = storage_query.query(StorageQueryInput(totalFuel))

    assert requests_mock.last_request is not None
    assert len(storage_output) == 1
    expected_deps = copy.deepcopy(JSON_OUTPUT["storageRental"][1])
    expected_deps["service"]["exclusiveUpstreamCompanies"] = ["hydrogen_nrmm:5"]
    expected_deps["service"]["exclusiveDownstreamCompanies"] = ["hydrogen_nrmm:6"]
    assert json.loads(storage_output[0].dumps()) == expected_deps
