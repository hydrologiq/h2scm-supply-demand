import json
from simulation.query.queries import (
    QueryConfiguration,
    LogisticQuery,
    LogisticQueryInput,
)
from requests_mock import Mocker
from tests.helpers.logistic import (
    LogisticResponse,
    logistic_query_response_json,
    sparql_query_logistic,
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
      "logistic": [
        {
          "service": { "id": "hydrogen_nrmm:1", "name": "Service 1" },
          "storage": { "id": "hydrogen_nrmm:12", "name": "Tube Trailer 1", "capacity": 300, "availableQuantity": 3 },
          "vehicle": { "id": "hydrogen_nrmm:123", "name": "Vehicle 1", "availableQuantity": 1, "transportDistance": 123 },
          "price": { "id": "hydrogen_nrmm:12345", "monetaryValue": 80 }
        },
        {
          "service": { "id": "hydrogen_nrmm:2", "name": "Service 2" },
          "storage": { "id": "hydrogen_nrmm:21", "name": "Tube Trailer 2", "capacity": 225, "availableQuantity": 1 },
          "vehicle": { "id": "hydrogen_nrmm:212", "name": "Vehicle 2", "availableQuantity": 2, "transportDistance": 123 },
          "price": { "id": "hydrogen_nrmm:214", "monetaryValue": 40 }
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


LOGISTIC_RESPONSE_1 = LogisticResponse(
    storage="12",
    storageName="Tube Trailer 1",
    storageAvailableQuantity=3,
    storageCapacity=300,
    vehicle="123",
    vehicleName="Vehicle 1",
    vehicleAvailableQuantity=1,
    vehicleTransportDistance=123,
    service="1",
    serviceName="Service 1",
    price="12345",
    priceMonetaryValue=80.0,
)

LOGISTIC_RESPONSE_2 = LogisticResponse(
    storage="21",
    storageName="Tube Trailer 2",
    storageAvailableQuantity=1,
    storageCapacity=225,
    vehicle="212",
    vehicleName="Vehicle 2",
    vehicleAvailableQuantity=2,
    vehicleTransportDistance=123,
    service="2",
    serviceName="Service 2",
    price="214",
    priceMonetaryValue=40.0,
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

    register_sparql_query_mock(
        requests_mock,
        sparql_query_logistic(minStorage),
        logistic_query_response_json([LOGISTIC_RESPONSE_1, LOGISTIC_RESPONSE_2]),
    )

    logistic_output = logistic_query.query(
        LogisticQueryInput(minStorage, BusinessOutputs.Storage.TubeTrailer)
    )

    assert requests_mock.last_request is not None
    assert len(logistic_output) == 2
    assert json.loads(logistic_output[0].dumps()) == JSON_OUTPUT["logistic"][0]
    assert json.loads(logistic_output[1].dumps()) == JSON_OUTPUT["logistic"][1]


LOGISTIC_RESPONSE_1_CO2e = LogisticResponse(
    storage="12",
    storageName="Tube Trailer 1",
    storageAvailableQuantity=3,
    storageCapacity=300,
    vehicle="123",
    vehicleName="Vehicle 1",
    vehicleAvailableQuantity=1,
    vehicleTransportDistance=123,
    service="1",
    serviceName="Service 1",
    serviceTransportCO2e=0.5,
    price="12345",
    priceMonetaryValue=80.0,
)

LOGISTIC_RESPONSE_2_CO2e = LogisticResponse(
    storage="21",
    storageName="Tube Trailer 2",
    storageAvailableQuantity=1,
    storageCapacity=225,
    vehicle="212",
    vehicleName="Vehicle 2",
    vehicleAvailableQuantity=2,
    vehicleTransportDistance=123,
    service="2",
    serviceName="Service 2",
    serviceTransportCO2e=1,
    price="214",
    priceMonetaryValue=40.0,
)


def test_run_logistic_query_with_co2e(requests_mock: Mocker):
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

    register_sparql_query_mock(
        requests_mock,
        sparql_query_logistic(minStorage),
        logistic_query_response_json(
            [LOGISTIC_RESPONSE_1_CO2e, LOGISTIC_RESPONSE_2_CO2e]
        ),
    )

    logistic_output = logistic_query.query(
        LogisticQueryInput(minStorage, BusinessOutputs.Storage.TubeTrailer)
    )

    assert requests_mock.last_request is not None
    assert len(logistic_output) == 2

    expected_logistic_1 = {**JSON_OUTPUT["logistic"][0]}
    expected_logistic_1["service"]["transportCO2e"] = 0.5
    assert json.loads(logistic_output[0].dumps()) == expected_logistic_1

    expected_logistic_2 = {**JSON_OUTPUT["logistic"][1]}
    expected_logistic_2["service"]["transportCO2e"] = 1
    assert json.loads(logistic_output[1].dumps()) == expected_logistic_2


LOGISTIC_RESPONSE_MCP = LogisticResponse(
    storage="12",
    storageName="MCP Option 1",
    storageAvailableQuantity=12,
    storageCapacity=16.0,
    vehicle="123",
    vehicleName="Vehicle 1",
    vehicleAvailableQuantity=1,
    vehicleTransportDistance=123,
    service="1",
    serviceName="Service 1",
    price="12345",
    priceMonetaryValue=80.0,
)

JSON_OUTPUT_MCP = json.loads(
    """
    {
      "logistic": [
        {
          "service": { "id": "hydrogen_nrmm:1", "name": "Service 1" },
          "storage": { "id": "hydrogen_nrmm:12", "name": "MCP Option 1", "capacity": 16, "availableQuantity": 12 },
          "vehicle": { "id": "hydrogen_nrmm:123", "name": "Vehicle 1", "availableQuantity": 1, "transportDistance": 123 },
          "price": { "id": "hydrogen_nrmm:12345", "monetaryValue": 80 }
        }
      ]
    }
    """
)


def test_run_logistic_query_with_mcp(requests_mock: Mocker):
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

    register_sparql_query_mock(
        requests_mock,
        sparql_query_logistic(
            minStorage, BusinessOutputs.Storage.ManifoldCylinderPallet
        ),
        logistic_query_response_json([LOGISTIC_RESPONSE_MCP]),
    )

    logistic_output = logistic_query.query(
        LogisticQueryInput(minStorage, BusinessOutputs.Storage.ManifoldCylinderPallet)
    )

    assert requests_mock.last_request is not None
    assert len(logistic_output) == 1
    assert json.loads(logistic_output[0].dumps()) == JSON_OUTPUT_MCP["logistic"][0]
