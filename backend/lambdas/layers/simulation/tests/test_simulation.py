import json

import pytest

from jsonschema import validate
from requests_mock import Mocker
from simulation.business import BusinessInput
from simulation.business.inputs import Fuel, Location
from simulation.logic.outputs import Matched
from simulation.query.queries import QueryConfiguration
from tests.helpers import (
    FuelResponse,
    LogisticResponse,
    logistic_query_response_json,
    fuel_query_response_json,
    sparql_query_fuel,
    sparql_query_logistic,
)

from simulation.run_simulation import run_simulation
from tests.helpers import to_id

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
    storage="1",
    storageName="Test Storage 1",
    storageAvailableQuantity=2,
    storageCapacity=4,
    vehicle="2",
    vehicleName="Vehicle 1",
    vehicleAvailableQuantity=1,
    vehicleTransportDistance=25,
    service="3",
    serviceName="Logistics Service 1",
    quote="5",
    quoteMonetaryValue=400,
)

FUEL_RESPONSE_1 = FuelResponse(
    producer="5",
    producerName="Producer 1",
    producerDailyOfftakeCapacity=300,
    dispenser="6",
    dispenserName="Dispensing Site 1",
    dispenserLat=54.99849,
    dispenserLong=-1.7691325,
    dispenserFillingStationCapacity=1,
    dispenserFillRate=10,
    service="7",
    serviceName="Fuel Service 1",
    quote="8",
    quoteMonetaryValue=40,
)


def test_simulation_no_results(requests_mock: Mocker):
    user_input = BusinessInput(
        location=Location(lat=55.0495388, long=-1.7529721), fuel=Fuel(300)
    )

    register_sparql_query_mock(
        requests_mock,
        sparql_query_logistic(300.0),
        logistic_query_response_json([]),
    )

    register_sparql_query_mock(
        requests_mock,
        sparql_query_fuel(300.0),
        fuel_query_response_json([]),
    )

    sim_output = run_simulation(
        user_input,
        QueryConfiguration(
            **{
                "scm_api_id": SCM_API_ID,
                "scm_api_region": SCM_API_REGION,
                "scm_api_stage": SCM_API_STAGE,
                "scm_repo": DEFAULT_REPO,
                "scm_access_token": MOCKED_ACCESS_TOKEN,
            }
        ),
    )

    assert sim_output is not None
    assert len(sim_output.fuel) == 0
    assert len(sim_output.logistic) == 0
    assert len(sim_output.matches) == 0


def test_base_simulation(requests_mock: Mocker):
    user_input = BusinessInput(
        location=Location(lat=55.0495388, long=-1.7529721), fuel=Fuel(300)
    )

    register_sparql_query_mock(
        requests_mock,
        sparql_query_logistic(300.0),
        logistic_query_response_json([LOGISTIC_RESPONSE_1]),
    )

    register_sparql_query_mock(
        requests_mock,
        sparql_query_fuel(300.0),
        fuel_query_response_json([FUEL_RESPONSE_1]),
    )

    sim_output = run_simulation(
        user_input,
        QueryConfiguration(
            **{
                "scm_api_id": SCM_API_ID,
                "scm_api_region": SCM_API_REGION,
                "scm_api_stage": SCM_API_STAGE,
                "scm_repo": DEFAULT_REPO,
                "scm_access_token": MOCKED_ACCESS_TOKEN,
            }
        ),
    )

    assert sim_output is not None
    assert len(sim_output.fuel) == 1
    assert sim_output.fuel[0].dumps() == FUEL_RESPONSE_1.query_response().dumps()
    assert len(sim_output.logistic) == 1
    assert (
        sim_output.logistic[0].dumps() == LOGISTIC_RESPONSE_1.query_response().dumps()
    )
    assert len(sim_output.matches) == 1
    ## fuelUtilisation = (300 / 300) * 100 = 100
    # price = (40 * 300) + (400 * 11.55) = 16620.0
    assert sim_output.matches[0] == Matched(
        logistic=to_id(LOGISTIC_RESPONSE_1.service),
        fuel=to_id(FUEL_RESPONSE_1.service),
        fuelUtilisation=100.0,
        price=16620.0,
        transportDistance=11.55,
    )


def test_simulation_no_results(requests_mock: Mocker):
    user_input = BusinessInput(
        location=Location(lat=55.0495388, long=-1.7529721), fuel=Fuel(300)
    )

    register_sparql_query_mock(
        requests_mock,
        sparql_query_logistic(300.0),
        logistic_query_response_json([LOGISTIC_RESPONSE_1]),
    )

    register_sparql_query_mock(
        requests_mock,
        sparql_query_fuel(300.0),
        fuel_query_response_json([]),
    )

    sim_output = run_simulation(
        user_input,
        QueryConfiguration(
            **{
                "scm_api_id": SCM_API_ID,
                "scm_api_region": SCM_API_REGION,
                "scm_api_stage": SCM_API_STAGE,
                "scm_repo": DEFAULT_REPO,
                "scm_access_token": MOCKED_ACCESS_TOKEN,
            }
        ),
    )

    assert sim_output is not None
    assert len(sim_output.fuel) == 0
    assert len(sim_output.logistic) == 1
    assert len(sim_output.matches) == 0
    sim_output_json = json.loads(sim_output.dumps())
    assert "fuel" in sim_output_json
    assert len(sim_output_json["fuel"]) == 0
    assert "matches" in sim_output_json
    assert len(sim_output_json["matches"]) == 0


def test_simulation_out_schema(requests_mock: Mocker):
    user_input = BusinessInput(
        location=Location(lat=55.0495388, long=-1.7529721), fuel=Fuel(300)
    )

    register_sparql_query_mock(
        requests_mock,
        sparql_query_logistic(300.0),
        logistic_query_response_json([LOGISTIC_RESPONSE_1]),
    )

    register_sparql_query_mock(
        requests_mock,
        sparql_query_fuel(300.0),
        fuel_query_response_json([FUEL_RESPONSE_1]),
    )

    sim_output = run_simulation(
        user_input,
        QueryConfiguration(
            **{
                "scm_api_id": SCM_API_ID,
                "scm_api_region": SCM_API_REGION,
                "scm_api_stage": SCM_API_STAGE,
                "scm_repo": DEFAULT_REPO,
                "scm_access_token": MOCKED_ACCESS_TOKEN,
            }
        ),
    )

    with open("tests/schema/SimulationResults.json") as schema:
        exception = False
        try:
            validate(
                instance=json.loads(sim_output.dumps()),
                schema=json.load(schema),
            )
        except Exception as e:
            print(e)
            exception = True
        assert exception == False
