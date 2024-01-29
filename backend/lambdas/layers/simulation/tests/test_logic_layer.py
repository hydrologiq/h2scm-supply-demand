import json
from simulation.business import BusinessOutput
from simulation.logic import LogicLayer
from simulation.query import QueryOutput

JSON_INPUT = json.loads(
    """
    {
      "logistic": [
        {
          "service": { "id": "hydrogen_nrmm:1", "name": "Service 1" },
          "storage": { "id": "hydrogen_nrmm:12", "name": "Tube Trailer 1", "capacity": 300, "availableQuantity": 3 },
          "vehicle": { "id": "hydrogen_nrmm:123", "name": "Vehicle 1", "availableQuantity": 1, "transportDistance": 123 },
          "distro":  { "id": "hydrogen_nrmm:1234", "name": "Vehicle Yard 1", "lat": 1, "long": 2 },
          "projectDistance": 12.345
        },
        {
          "service": { "id": "hydrogen_nrmm:2", "name": "Service 2" },
          "storage": { "id": "hydrogen_nrmm:21", "name": "Tube Trailer 2", "capacity": 225, "availableQuantity": 1 },
          "vehicle": { "id": "hydrogen_nrmm:212", "name": "Vehicle 2", "availableQuantity": 2, "transportDistance": 123 },
          "distro":  { "id": "hydrogen_nrmm:213", "name": "Vehicle Yard 2", "lat": 2, "long": 3 },
          "projectDistance": 54.321
        }
      ],
      "fuel": [
        {
          "service": { "id": "hydrogen_nrmm:3", "name": "Fuel Service 1" },
          "dispenser": { "id": "hydrogen_nrmm:31", "name": "Dispensing Site 1", "fillRate": 10, "fillingStationCapacity": 3, "lat": 3, "long": 4 },
          "producer": { "id": "hydrogen_nrmm:312", "name": "Hydrogen Producer 1", "dailyOfftakeCapacity": 600 }
        }
      ]
    }
    """
)


def test_run_logic_layer_output():
    logic_input = QueryOutput(**JSON_INPUT)
    business_output = BusinessOutput(
        **{
            "fuel": [
                {"type": "TubeTrailer", "amount": 300},
                {"type": "TubeTrailer", "amount": 185},
            ],
            "project": {"location": {"lat": 12.234, "long": 43.221}},
        }
    )
    logic_layer = LogicLayer()

    logic_output = logic_layer.run(logic_input, business_output)

    # Second only matches as within transport range (97 miles vs 194 miles)
    # redundancy -> (485 / 600) * 100 = 80.8333333333333
    assert json.loads(logic_output.dumps()) == {
        "logistic": [
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
                "distro": {
                    "id": "hydrogen_nrmm:213",
                    "name": "Vehicle Yard 2",
                    "lat": 2,
                    "long": 3,
                },
                "projectDistance": 54.321,
            },
        ],
        "fuel": [
            {
                "service": {"id": "hydrogen_nrmm:3", "name": "Fuel Service 1"},
                "dispenser": {
                    "id": "hydrogen_nrmm:31",
                    "name": "Dispensing Site 1",
                    "fillRate": 10,
                    "fillingStationCapacity": 3,
                    "lat": 3,
                    "long": 4,
                },
                "producer": {
                    "id": "hydrogen_nrmm:312",
                    "name": "Hydrogen Producer 1",
                    "dailyOfftakeCapacity": 600,
                },
            }
        ],
        "matches": [
            {
                "logistic": "hydrogen_nrmm:2",
                "fuel": "hydrogen_nrmm:3",
                "redundancy": 80.83,
            }
        ],
    }
