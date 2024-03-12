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


STORAGE_RESPONSE_1 = StorageResponse(
    storage="12",
    storageName="Tube Trailer 1",
    storageAvailableQuantity=3,
    storageCapacity=300,
    service="1",
    serviceName="Service 1",
    quote="12345",
    quoteMonetaryValuePerUnit=80.0,
    quoteCurrency="GBP",
    quoteUnit="item",
    company="15",
)

STORAGE_RESPONSE_2 = StorageResponse(
    storage="21",
    storageName="Tube Trailer 2",
    storageAvailableQuantity=1,
    storageCapacity=225,
    service="2",
    serviceName="Service 2",
    quote="214",
    quoteMonetaryValuePerUnit=40.0,
    quoteCurrency="GBP",
    quoteUnit="item",
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
        storage_query_response_json([STORAGE_RESPONSE_1, STORAGE_RESPONSE_2]),
    )

    storage_output = storage_query.query(StorageQueryInput(totalFuel))

    assert requests_mock.last_request is not None
    assert len(storage_output) == 2
    assert (
        storage_output[0].to_object() == STORAGE_RESPONSE_1.query_response().to_object()
    )
    assert (
        storage_output[1].to_object() == STORAGE_RESPONSE_2.query_response().to_object()
    )


STORAGE_RESPONSE_MCP = StorageResponse(
    storage="12",
    storageName="MCP Option 1",
    storageAvailableQuantity=12,
    storageCapacity=16.0,
    service="1",
    serviceName="Service 1",
    quote="12345",
    quoteMonetaryValuePerUnit=80.0,
    quoteCurrency="GBP",
    quoteUnit="item",
    company="15",
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
        storage_query_response_json([STORAGE_RESPONSE_MCP]),
    )

    storage_output = storage_query.query(StorageQueryInput(totalFuel))

    assert requests_mock.last_request is not None
    assert len(storage_output) == 1
    assert (
        storage_output[0].to_object()
        == STORAGE_RESPONSE_MCP.query_response().to_object()
    )


STORAGE_RESPONSE_2_DEPS = StorageResponse(
    storage="21",
    storageName="Tube Trailer 2",
    storageAvailableQuantity=1,
    storageCapacity=225,
    service="2",
    serviceName="Service 2",
    quote="214",
    quoteMonetaryValuePerUnit=40.0,
    quoteCurrency="GBP",
    quoteUnit="item",
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
        storage_query_response_json([STORAGE_RESPONSE_2_DEPS]),
    )

    storage_output = storage_query.query(StorageQueryInput(totalFuel))

    assert requests_mock.last_request is not None
    assert len(storage_output) == 1
    assert (
        storage_output[0].to_object()
        == STORAGE_RESPONSE_2_DEPS.query_response().to_object()
    )
