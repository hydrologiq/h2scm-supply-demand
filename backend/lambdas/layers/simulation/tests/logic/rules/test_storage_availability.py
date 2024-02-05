from simulation.logic.logic_input import LogicInput
from simulation.logic.rules.filter import (
    StorageAvailabilityRule,
)
from simulation.query import QueryInput

SAMPLE_LOGIC_INPUT = {
    "logistic": [],
    "fuel": [],
    "storageRental": [
        {
            "quote": {"id": "hydrogen_nrmm:5", "monetaryValue": 40},
            "service": {"id": "hydrogen_nrmm:4", "name": "Storage Service 2"},
            "storage": {
                "id": "hydrogen_nrmm:41",
                "name": "TubeTrailer 1",
                "availableQuantity": 3,
                "capacity": 300,
            },
        },
        {
            "quote": {"id": "hydrogen_nrmm:6", "monetaryValue": 400},
            "service": {"id": "hydrogen_nrmm:3", "name": "Storage Service 1"},
            "storage": {
                "id": "hydrogen_nrmm:31",
                "name": "MCP 1",
                "availableQuantity": 5,
                "capacity": 16.5,
            },
        },
    ],
}


def test_filters_available_storage_rentals():
    query_input = QueryInput(
        **{
            "fuel": [
                {"type": "TubeTrailer", "amount": 300},
                {"type": "TubeTrailer", "amount": 300},
                {"type": "TubeTrailer", "amount": 300},
            ],
            "project": {"location": {"lat": 12.234, "long": 43.221}},
        }
    )
    logic_input = LogicInput(**SAMPLE_LOGIC_INPUT)

    rule = StorageAvailabilityRule()

    rule_output = rule.apply(logic_input, query_input)

    assert len(logic_input.storageRental) == 2
    assert len(rule_output.storageRental) == 1
    assert rule_output.storageRental[0] == logic_input.storageRental[0]
