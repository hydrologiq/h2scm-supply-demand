import json
from api_run_simulation.simulation.logic.logic_input import LogicInput
from api_run_simulation.simulation.logic.rules.filter import DistanceFromProjectRule
from api_run_simulation.simulation.query import QueryInput

SAMPLE_LOGIC_INPUT = {
    "logistic": [
        {
            "service": {"id": "hydrogen_nrmm:1", "name": "Service 1"},
            "storage": {
                "id": "hydrogen_nrmm:12",
                "name": "Tube Trailer 1",
                "capacity": 300,
                "availableQuantity": 3,
            },
            "vehicle": {
                "id": "hydrogen_nrmm:123",
                "name": "Vehicle 1",
                "availableQuantity": 1,
                "transportDistance": 123,
            },
            "projectDistance": 12.345,
        },
        {
            "service": {"id": "hydrogen_nrmm:2", "name": "Service 2"},
            "storage": {
                "id": "hydrogen_nrmm:21",
                "name": "Tube Trailer 2",
                "capacity": 225,
                "availableQuantity": 1,
            },
            "vehicle": {
                "id": "hydrogen_nrmm:212",
                "name": "Vehicle 2",
                "availableQuantity": 2,
                "transportDistance": 123,
            },
            "projectDistance": 555,
        },
    ],
    "fuel": [],
}


def test_filters_transport_project_distance():
    query_input = QueryInput(
        **{
            "fuel": [
                {"type": "TubeTrailer", "amount": 300},
                {"type": "TubeTrailer", "amount": 185},
            ],
            "project": {"location": {"lat": 12.234, "long": 43.221}},
        }
    )
    logic_input = LogicInput(**SAMPLE_LOGIC_INPUT)

    rule = DistanceFromProjectRule(query_input)

    rule_output = rule.apply(logic_input)

    assert len(logic_input.logistic) == 2
    assert len(rule_output.logistic) == 1
    assert rule_output.logistic[0] == logic_input.logistic[0]
