import json
from requests_mock import Mocker
from simulation.query.queries.base_query import BaseQuery
from simulation.query.queries.query_configuration import QueryConfiguration

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
    graphs: list[str] = ["default"],
):
    return requests_mock.register_uri(
        "POST",
        f"https://{SCM_API_ID}.execute-api.{SCM_API_REGION}.amazonaws.com/{SCM_API_STAGE}/repositories/{repo}/query/select?graphs={','.join(graphs)}",
        request_headers={
            "Authorization": f"Bearer {MOCKED_ACCESS_TOKEN}",
        },
        status_code=status_code,
        additional_matcher=lambda request: request.text == query,
        json=response,
    )


def test_query_graphs(requests_mock: Mocker):
    base_query = BaseQuery(
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
    graphs = ["default", "holy_moly"]
    register_sparql_query_mock(requests_mock, "blank", json.dumps({}), graphs=graphs)

    response = base_query.query(graphs=graphs)
    assert len(response) == 0
