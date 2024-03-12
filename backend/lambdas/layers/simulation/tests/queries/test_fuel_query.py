import copy
import pytest
from simulation.query.queries import (
    QueryConfiguration,
    FuelQuery,
    FuelQueryInput,
)
from requests_mock import Mocker
from tests.helpers.fuel import FuelResponse, fuel_query_response_json, sparql_query_fuel
import simulation.business.outputs as BusinessOutputs

FUEL_RESPONSE_1 = FuelResponse(
    producer="312",
    producerName="Hydrogen Producer 1",
    producerWeeklyProductionCapacity=600,
    producerType=BusinessOutputs.Producer.ElectrolyticHydrogen,
    dispenser="31",
    dispenserName="Dispensing Site 1",
    dispenserLat=123,
    dispenserLong=43.2,
    service="3",
    serviceName="Fuel Service 1",
    quote="4",
    quoteMonetaryValuePerUnit=40.0,
    quoteCurrency="GBP",
    quoteUnit="kg",
    company="5",
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
        f"https://{SCM_API_ID}.execute-api.{SCM_API_REGION}.amazonaws.com/{SCM_API_STAGE}/repositories/{repo}/query/select?graphs=default&named=true",
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
        fuel_query.query(
            FuelQueryInput(fuel_total, [BusinessOutputs.Storage.TubeTrailer])
        )
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
        fuel_query.query(
            FuelQueryInput(fuel_total, [BusinessOutputs.Storage.TubeTrailer])
        )
    assert (
        str(e_info.value)
        == "400 Client Error: None for url: https://abcdef.execute-api.eu-west-2.amazonaws.com/dev/repositories/live/query/select?graphs=default&named=true"
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
        fuel_query_response_json([FUEL_RESPONSE_1]),
    )

    fuel_output = fuel_query.query(
        FuelQueryInput(fuel_total, [BusinessOutputs.Storage.TubeTrailer])
    )

    assert requests_mock.last_request is not None
    assert len(fuel_output) == 1
    assert fuel_output[0].to_object() == FUEL_RESPONSE_1.query_response().to_object()


def test_run_fuel_query_with_multiple_stored_in(requests_mock: Mocker):
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
    fuel_mcp_tt = copy.deepcopy(FUEL_RESPONSE_1)
    fuel_mcp_tt.producerStoredIn.append(BusinessOutputs.Storage.ManifoldCylinderPallet)
    register_sparql_query_mock(
        requests_mock,
        sparql_query_fuel(
            fuel_total,
            [
                BusinessOutputs.Storage.TubeTrailer,
                BusinessOutputs.Storage.ManifoldCylinderPallet,
            ],
        ),
        fuel_query_response_json([fuel_mcp_tt]),
    )

    fuel_output = fuel_query.query(
        FuelQueryInput(
            fuel_total,
            [
                BusinessOutputs.Storage.TubeTrailer,
                BusinessOutputs.Storage.ManifoldCylinderPallet,
            ],
        )
    )

    assert requests_mock.last_request is not None
    assert len(fuel_output) == 1
    assert fuel_output[0].to_object() == FUEL_RESPONSE_1.query_response().to_object()


FUEL_RESPONSE_1_CO2e = FuelResponse(
    producer="312",
    producerName="Hydrogen Producer 1",
    producerWeeklyProductionCapacity=600,
    producerProductionCO2e=10,
    producerType=BusinessOutputs.Producer.ElectrolyticHydrogen,
    dispenser="31",
    dispenserName="Dispensing Site 1",
    dispenserLat=123,
    dispenserLong=43.2,
    service="3",
    serviceName="Fuel Service 1",
    quote="4",
    quoteMonetaryValuePerUnit=40.0,
    quoteCurrency="GBP",
    quoteUnit="kg",
    company="5",
)


def test_run_fuel_query_with_co2e(requests_mock: Mocker):
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
        fuel_query_response_json([FUEL_RESPONSE_1_CO2e]),
    )

    fuel_output = fuel_query.query(
        FuelQueryInput(fuel_total, [BusinessOutputs.Storage.TubeTrailer])
    )

    assert requests_mock.last_request is not None
    assert len(fuel_output) == 1
    assert (
        fuel_output[0].to_object() == FUEL_RESPONSE_1_CO2e.query_response().to_object()
    )


FUEL_RESPONSE_1_DEPS = FuelResponse(
    producer="312",
    producerName="Hydrogen Producer 1",
    producerWeeklyProductionCapacity=600,
    producerType=BusinessOutputs.Producer.ElectrolyticHydrogen,
    dispenser="31",
    dispenserName="Dispensing Site 1",
    dispenserLat=123,
    dispenserLong=43.2,
    service="3",
    serviceName="Fuel Service 1",
    quote="4",
    quoteMonetaryValuePerUnit=40.0,
    quoteCurrency="GBP",
    quoteUnit="kg",
    company="5",
    serviceExclusiveUpstreamCompanies="5",
    serviceExclusiveDownstreamCompanies="6",
)


def test_run_fuel_query_with_deps(requests_mock: Mocker):
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
        fuel_query_response_json([FUEL_RESPONSE_1_DEPS]),
    )

    fuel_output = fuel_query.query(
        FuelQueryInput(fuel_total, [BusinessOutputs.Storage.TubeTrailer])
    )

    assert requests_mock.last_request is not None
    assert len(fuel_output) == 1
    assert (
        fuel_output[0].to_object() == FUEL_RESPONSE_1_DEPS.query_response().to_object()
    )
