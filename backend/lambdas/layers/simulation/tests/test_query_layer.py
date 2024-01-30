import json

from mock import patch
from simulation.query.queries import (
    QueryConfiguration,
    LogisticQueryResponse,
    LogisticQueryInput,
    FuelQueryInput,
    FuelQueryResponse,
)

from simulation.query import QueryInput, QueryLayer
from requests_mock import Mocker
from tests.data import (
    SPARQL_QUERY_LOGISTIC_RESPONSE,
    sparql_query_logistic,
)

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
          "price": { "id": "hydrogen_nrmm:12345", "monetaryValue": 40}
        },
        {
          "service": { "id": "hydrogen_nrmm:2", "name": "Service 2" },
          "storage": { "id": "hydrogen_nrmm:21", "name": "Tube Trailer 2", "capacity": 225, "availableQuantity": 1 },
          "vehicle": { "id": "hydrogen_nrmm:212", "name": "Vehicle 2", "availableQuantity": 2, "transportDistance": 123 },
          "price": { "id": "hydrogen_nrmm:2124", "monetaryValue": 40}
        }
      ],
      "fuel": [
        {
          "price": { "id": "hydrogen_nrmm:314", "monetaryValue": 40},
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


def test_run_query_layer_output():
    with patch(
        "simulation.query.queries.logistic_query.LogisticQuery.query"
    ) as logistics_patched:
        logistics_patched.return_value = [
            LogisticQueryResponse(**logistic_entry)
            for logistic_entry in JSON_OUTPUT["logistic"]
        ]
        with patch(
            "simulation.query.queries.fuel_query.FuelQuery.query"
        ) as fuel_patched:
            fuel_patched.return_value = [
                FuelQueryResponse(**fuel_entry) for fuel_entry in JSON_OUTPUT["fuel"]
            ]
            query_input = QueryInput(**JSON_INPUT)
            query_layer = QueryLayer(
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

            user_output = query_layer.run(query_input)

            logistics_patched.assert_called_once_with(LogisticQueryInput(185))
            fuel_patched.assert_called_once_with(FuelQueryInput(485))
            assert json.loads(user_output.dumps()) == JSON_OUTPUT
