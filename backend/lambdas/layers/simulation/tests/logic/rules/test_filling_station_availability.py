import json
from simulation.logic.logic_input import LogicInput
from simulation.logic.rules.filter import (
    FillingStationAvailabilityRule,
)
from simulation.query import QueryInput

SAMPLE_LOGIC_INPUT = {
    "logistic": [],
    "fuel": [
        {
            "company": {"id": "hydrogen_nrmm:5"},
            "quote": {"id": "hydrogen_nrmm:5", "monetaryValuePerUnit": 40},
            "service": {"id": "hydrogen_nrmm:4", "name": "Fuel Service 2"},
            "dispenser": {
                "id": "hydrogen_nrmm:41",
                "name": "Dispensing Site 2",
                "fillRate": 12,
                "fillingStationCapacity": 1,
                "lat": 32.1,
                "long": 12.3,
            },
            "producer": {
                "id": "hydrogen_nrmm:412",
                "name": "Hydrogen Producer 2",
                "dailyOfftakeCapacity": 300,
            },
        },
        {
            "company": {"id": "hydrogen_nrmm:7"},
            "quote": {"id": "hydrogen_nrmm:6", "monetaryValuePerUnit": 400},
            "service": {"id": "hydrogen_nrmm:3", "name": "Fuel Service 1"},
            "dispenser": {
                "id": "hydrogen_nrmm:31",
                "name": "Dispensing Site 1",
                "fillRate": 10,
                "fillingStationCapacity": 3,
                "lat": 123,
                "long": 43.2,
            },
            "producer": {
                "id": "hydrogen_nrmm:312",
                "name": "Hydrogen Producer 1",
                "dailyOfftakeCapacity": 600,
            },
        },
    ],
    "storageRental": [],
}


def test_filters_available_filling_stations():
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

    rule = FillingStationAvailabilityRule()

    rule_output = rule.apply(logic_input, query_input)

    assert len(logic_input.fuel) == 2
    assert len(rule_output.fuel) == 1
    assert rule_output.fuel[0] == logic_input.fuel[1]
