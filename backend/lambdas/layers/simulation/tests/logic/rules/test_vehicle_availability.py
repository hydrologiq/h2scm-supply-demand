import json
from simulation.logic.logic_input import LogicInput
from simulation.logic.rules.filter import VehicleAvailabilityRule
from simulation.query import QueryInput

SAMPLE_LOGIC_INPUT = {
    "logistic": [
        {
            "service": {"id": "hydrogen_nrmm:1", "name": "Service 1"},
            "vehicle": {
                "id": "hydrogen_nrmm:123",
                "name": "Vehicle 1",
                "availableQuantity": 1,
                "transportDistance": 123,
            },
            "quote": {"id": "hydrogen_nrmm:1234", "monetaryValue": 80},
        },
        {
            "service": {"id": "hydrogen_nrmm:2", "name": "Service 2"},
            "vehicle": {
                "id": "hydrogen_nrmm:212",
                "name": "Vehicle 2",
                "availableQuantity": 2,
                "transportDistance": 123,
            },
            "quote": {"id": "hydrogen_nrmm:2134", "monetaryValue": 40},
        },
    ],
    "fuel": [],
}


def test_filters_out_vehicle():
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

    rule = VehicleAvailabilityRule()

    rule_output = rule.apply(logic_input, query_input)

    assert len(logic_input.logistic) == 2
    assert len(rule_output.logistic) == 1
    assert rule_output.logistic[0] == logic_input.logistic[1]
