from requests_mock import Mocker
from simulation.business import BusinessInput
from simulation.business.inputs import Fuel, Location
from simulation.logic.outputs import Matched
from simulation.query.queries import QueryConfiguration
from tests.helpers import (
    FuelResponse,
    LogisticResponse,
    logistic_query_sparql,
    logistic_query_response_json,
    fuel_query_sparql,
    fuel_query_response_json,
)

from run_simulation import run_simulation
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
    projectDistance=4.095,
    distro="4",
    distroName="Vehicle Yard 1",
    distroLat=55.0144661,
    distroLong=-1.669601,
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
)


def test_base_simulation(requests_mock: Mocker):
    user_input = BusinessInput(
        location=Location(lat=55.0495388, long=-1.7529721), fuel=Fuel(300)
    )

    register_sparql_query_mock(
        requests_mock,
        logistic_query_sparql(300.0, user_input.location.lat, user_input.location.long),
        logistic_query_response_json([LOGISTIC_RESPONSE_1]),
    )

    register_sparql_query_mock(
        requests_mock,
        fuel_query_sparql(300.0),
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
    ## redundancy = (300 / 300 - 1) * 100 = 0
    assert sim_output.matches[0] == Matched(
        logistic=to_id(LOGISTIC_RESPONSE_1.service),
        fuel=to_id(FUEL_RESPONSE_1.service),
        redundancy=0.0,
    )
