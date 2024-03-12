import json

from jsonschema import validate
from requests_mock import Mocker
from simulation.business import BusinessInput
from simulation.business.inputs import Fuel, Location
from simulation.logic.outputs import Matched
from simulation.logic.outputs.matched import (
    Breakdown,
    BreakdownItem,
    MatchedInstance,
    Production,
    ProductionCapacity,
    ServiceType,
)
from simulation.query.queries import QueryConfiguration
from tests.helpers import (
    FuelResponse,
    LogisticResponse,
    StorageResponse,
    logistic_query_response_json,
    fuel_query_response_json,
    storage_query_response_json,
    sparql_query_fuel,
    sparql_query_logistic,
    sparql_query_storage,
)

from simulation.run_simulation import run_simulation
from tests.helpers import to_id
import simulation.business.outputs as BusinessOutputs

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
    graphs: list[str] = ["default"],
):
    return requests_mock.register_uri(
        "POST",
        f"https://{SCM_API_ID}.execute-api.{SCM_API_REGION}.amazonaws.com/{SCM_API_STAGE}/repositories/{repo}/query/select?graphs={','.join(graphs)}",
        request_headers={
            "Authorization": f"Bearer {MOCKED_ACCESS_TOKEN}",
        },
        status_code=200,
        additional_matcher=lambda request: request.text == query,
        json=response,
    )


LOGISTIC_RESPONSE_1 = LogisticResponse(
    vehicle="2",
    vehicleName="Vehicle 1",
    vehicleAvailableQuantity=1,
    vehicleTransportDistance=25,
    service="3",
    serviceName="Logistics Service 1",
    quote="5",
    quoteMonetaryValuePerUnit=400,
    quoteCurrency="GBP",
    quoteUnit="trip",
    company="25",
)

STORAGE_RESPONSE_1 = StorageResponse(
    storage="10",
    storageName="Vehicle 1",
    storageAvailableQuantity=1,
    storageCapacity=600,
    service="3",
    serviceName="Storage Service 1",
    quote="5",
    quoteMonetaryValuePerUnit=1000,
    quoteCurrency="GBP",
    quoteUnit="week",
    storageType=BusinessOutputs.Storage.TubeTrailer,
    company="11",
)

FUEL_RESPONSE_1 = FuelResponse(
    producer="5",
    producerName="Producer 1",
    producerWeeklyProductionCapacity=300,
    producerType=BusinessOutputs.Producer.ElectrolyticHydrogen,
    dispenser="6",
    dispenserName="Dispensing Site 1",
    dispenserLat=54.99849,
    dispenserLong=-1.7691325,
    service="7",
    serviceName="Fuel Service 1",
    quote="8",
    quoteMonetaryValuePerUnit=40,
    quoteCurrency="GBP",
    quoteUnit="kg",
    company="9",
)


def test_simulation_no_results(requests_mock: Mocker):
    user_input = BusinessInput(
        location=Location(lat=55.0495388, long=-1.7529721), fuel=Fuel(300)
    )

    register_sparql_query_mock(
        requests_mock,
        sparql_query_storage(300.0),
        storage_query_response_json([]),
    )

    register_sparql_query_mock(
        requests_mock,
        sparql_query_logistic([]),
        logistic_query_response_json([]),
    )

    register_sparql_query_mock(
        requests_mock,
        sparql_query_fuel(300.0, []),
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
    assert len(sim_output.storageRental) == 0
    assert len(sim_output.matches) == 0


def test_base_simulation(requests_mock: Mocker):
    user_input = BusinessInput(
        location=Location(lat=55.0495388, long=-1.7529721), fuel=Fuel(300.0)
    )

    register_sparql_query_mock(
        requests_mock,
        sparql_query_storage(300.0),
        storage_query_response_json([STORAGE_RESPONSE_1]),
    )

    register_sparql_query_mock(
        requests_mock,
        sparql_query_logistic(),
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
    assert len(sim_output.storageRental) == 1
    assert (
        sim_output.storageRental[0].dumps()
        == STORAGE_RESPONSE_1.query_response().dumps()
    )
    assert len(sim_output.matches) == 1
    assert sim_output.matches[0] == Matched(
        logistic=MatchedInstance(
            to_id(LOGISTIC_RESPONSE_1.service),
            LOGISTIC_RESPONSE_1.serviceName,
            False,
            False,
            "hydrogen_nrmm:",
        ),
        fuel=MatchedInstance(
            to_id(FUEL_RESPONSE_1.service),
            FUEL_RESPONSE_1.serviceName,
            False,
            False,
            "hydrogen_nrmm:",
        ),
        cost=Breakdown(
            total=13400.0,
            breakdown=[
                BreakdownItem(
                    ServiceType.fuel,
                    to_id(FUEL_RESPONSE_1.service),
                    300.0,
                    40.0,
                    "kg",
                    "GBP",
                ),
                BreakdownItem(
                    ServiceType.storageRental,
                    to_id(STORAGE_RESPONSE_1.service),
                    1.0,
                    1000.0,
                    "week",
                    "GBP",
                ),
                BreakdownItem(
                    ServiceType.logistic,
                    to_id(LOGISTIC_RESPONSE_1.service),
                    1.0,
                    400.0,
                    "trip",
                    "GBP",
                ),
            ],
        ),
        production=Production(
            capacity=ProductionCapacity(weekly=300.0, weeklyUsed=100.0),
            method=BusinessOutputs.Producer.ElectrolyticHydrogen,
            location=Location(
                lat=54.99849,
                long=-1.7691325,
            ),
        ),
        transportDistance=11.55,
        storage=MatchedInstance(
            to_id(STORAGE_RESPONSE_1.service),
            STORAGE_RESPONSE_1.serviceName,
            False,
            False,
            "hydrogen_nrmm:",
            BusinessOutputs.Storage.TubeTrailer,
        ),
    )


def test_simulation_no_matches(requests_mock: Mocker):
    user_input = BusinessInput(
        location=Location(lat=55.0495388, long=-1.7529721), fuel=Fuel(300)
    )

    register_sparql_query_mock(
        requests_mock,
        sparql_query_storage(300.0),
        storage_query_response_json([STORAGE_RESPONSE_1]),
    )

    register_sparql_query_mock(
        requests_mock,
        sparql_query_logistic(),
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
    assert len(sim_output.storageRental) == 1
    assert len(sim_output.matches) == 0
    sim_output_json = json.loads(sim_output.dumps())
    assert "fuel" in sim_output_json
    assert len(sim_output_json["fuel"]) == 0
    assert "matches" in sim_output_json
    assert len(sim_output_json["matches"]) == 0


def test_simulation_out_schema(requests_mock: Mocker):
    user_input = BusinessInput(
        location=Location(lat=55.0495388, long=-1.7529721), fuel=Fuel(amount=300)
    )
    graphs = ["default", "abc"]

    register_sparql_query_mock(
        requests_mock,
        sparql_query_storage(300.0),
        storage_query_response_json([STORAGE_RESPONSE_1]),
        graphs=graphs,
    )

    register_sparql_query_mock(
        requests_mock,
        sparql_query_logistic(),
        logistic_query_response_json([LOGISTIC_RESPONSE_1]),
        graphs=graphs,
    )

    register_sparql_query_mock(
        requests_mock,
        sparql_query_fuel(300.0),
        fuel_query_response_json([FUEL_RESPONSE_1]),
        graphs=graphs,
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
        graphs=graphs,
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
