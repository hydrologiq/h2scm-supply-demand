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
    vehicle="123",
    vehicleName="Vehicle 1",
    vehicleAvailableQuantity=1,
    vehicleTransportDistance=123,
    service="1",
    serviceName="Service 1",
    quote="12345",
    quoteMonetaryValuePerUnit=80.0,
    quoteCurrency="GBP",
    quoteUnit="trip",
    company="15",
)

LOGISTIC_RESPONSE_2 = LogisticResponse(
    vehicle="212",
    vehicleName="Vehicle 2",
    vehicleAvailableQuantity=2,
    vehicleTransportDistance=123,
    service="2",
    serviceName="Service 2",
    quote="214",
    quoteMonetaryValuePerUnit=40.0,
    quoteCurrency="GBP",
    quoteUnit="trip",
    company="25",
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

    register_sparql_query_mock(
        requests_mock,
        sparql_query_logistic(),
        logistic_query_response_json([LOGISTIC_RESPONSE_1, LOGISTIC_RESPONSE_2]),
    )

    logistic_output = logistic_query.query(
        LogisticQueryInput([BusinessOutputs.Storage.TubeTrailer])
    )

    assert requests_mock.last_request is not None
    assert len(logistic_output) == 2
    assert (
        logistic_output[0].to_object()
        == LOGISTIC_RESPONSE_1.query_response().to_object()
    )
    assert (
        logistic_output[1].to_object()
        == LOGISTIC_RESPONSE_2.query_response().to_object()
    )


LOGISTIC_RESPONSE_1_CO2e = LogisticResponse(
    vehicle="123",
    vehicleName="Vehicle 1",
    vehicleAvailableQuantity=1,
    vehicleTransportDistance=123,
    service="1",
    serviceName="Service 1",
    serviceTransportCO2e=0.5,
    quote="12345",
    quoteMonetaryValuePerUnit=80.0,
    quoteCurrency="GBP",
    quoteUnit="trip",
    company="15",
)

LOGISTIC_RESPONSE_2_CO2e = LogisticResponse(
    vehicle="212",
    vehicleName="Vehicle 2",
    vehicleAvailableQuantity=2,
    vehicleTransportDistance=123,
    service="2",
    serviceName="Service 2",
    serviceTransportCO2e=1,
    quote="214",
    quoteMonetaryValuePerUnit=40.0,
    quoteCurrency="GBP",
    quoteUnit="trip",
    company="25",
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

    register_sparql_query_mock(
        requests_mock,
        sparql_query_logistic(),
        logistic_query_response_json(
            [LOGISTIC_RESPONSE_1_CO2e, LOGISTIC_RESPONSE_2_CO2e]
        ),
    )

    logistic_output = logistic_query.query(
        LogisticQueryInput([BusinessOutputs.Storage.TubeTrailer])
    )

    assert requests_mock.last_request is not None
    assert len(logistic_output) == 2
    assert (
        logistic_output[0].to_object()
        == LOGISTIC_RESPONSE_1_CO2e.query_response().to_object()
    )
    assert (
        logistic_output[1].to_object()
        == LOGISTIC_RESPONSE_2_CO2e.query_response().to_object()
    )


LOGISTIC_RESPONSE_MCP = LogisticResponse(
    vehicle="123",
    vehicleName="Vehicle 1",
    vehicleAvailableQuantity=1,
    vehicleTransportDistance=123,
    service="1",
    serviceName="Service 1",
    quote="12345",
    quoteMonetaryValuePerUnit=80.0,
    quoteCurrency="GBP",
    quoteUnit="trip",
    company="15",
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

    register_sparql_query_mock(
        requests_mock,
        sparql_query_logistic([BusinessOutputs.Storage.ManifoldCylinderPallet]),
        logistic_query_response_json([LOGISTIC_RESPONSE_MCP]),
    )

    logistic_output = logistic_query.query(
        LogisticQueryInput([BusinessOutputs.Storage.ManifoldCylinderPallet])
    )

    assert requests_mock.last_request is not None
    assert len(logistic_output) == 1
    assert (
        logistic_output[0].to_object()
        == LOGISTIC_RESPONSE_MCP.query_response().to_object()
    )


LOGISTIC_RESPONSE_DEPS = LogisticResponse(
    vehicle="123",
    vehicleName="Vehicle 1",
    vehicleAvailableQuantity=1,
    vehicleTransportDistance=123,
    service="1",
    serviceName="Service 1",
    quote="12345",
    quoteMonetaryValuePerUnit=80.0,
    quoteCurrency="GBP",
    quoteUnit="trip",
    company="15",
    serviceExclusiveUpstreamCompanies="5",
    serviceExclusiveDownstreamCompanies="6",
)


def test_run_logistic_query_with_deps(requests_mock: Mocker):
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

    register_sparql_query_mock(
        requests_mock,
        sparql_query_logistic(),
        logistic_query_response_json([LOGISTIC_RESPONSE_DEPS]),
    )

    logistic_output = logistic_query.query(
        LogisticQueryInput([BusinessOutputs.Storage.TubeTrailer])
    )

    assert requests_mock.last_request is not None
    assert len(logistic_output) == 1
    assert (
        logistic_output[0].to_object()
        == LOGISTIC_RESPONSE_DEPS.query_response().to_object()
    )
