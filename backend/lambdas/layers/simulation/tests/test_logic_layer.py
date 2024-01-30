import json

from jsonschema import validate
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
          "vehicle": { "id": "hydrogen_nrmm:123", "name": "Vehicle 1", "availableQuantity": 1, "transportDistance": 110 },
          "price": { "id": "hydrogen_nrmm:12345", "monetaryValue": 80}
        },
        {
          "service": { "id": "hydrogen_nrmm:2", "name": "Service 2" },
          "storage": { "id": "hydrogen_nrmm:21", "name": "Tube Trailer 2", "capacity": 225, "availableQuantity": 1 },
          "vehicle": { "id": "hydrogen_nrmm:212", "name": "Vehicle 2", "availableQuantity": 2, "transportDistance": 123 },
          "price": { "id": "hydrogen_nrmm:2134", "monetaryValue": 40}
        }
      ],
      "fuel": [
        {          
          "price": { "id": "hydrogen_nrmm:314", "monetaryValue": 40},
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
            "project": {"location": {"lat": 3, "long": 4.5}},
        }
    )
    logic_layer = LogicLayer()

    logic_output = logic_layer.run(logic_input, business_output)

    # Second only matches as within transport range (110 vs 123 km)
    # fuelUtilisation -> (485 / 600) * 100 = 80.8333333333333
    # price -> (485 * 40) + (111.17 * 40) = 23846.8
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
                "price": {"id": "hydrogen_nrmm:2134", "monetaryValue": 40},
            },
        ],
        "fuel": [
            {
                "price": {"id": "hydrogen_nrmm:314", "monetaryValue": 40},
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
                "fuelUtilisation": 80.83,
                "price": 23846.8,
                "transportDistance": 111.17,
            }
        ],
    }


def test_run_logic_layer_output_with_co2e():
    input_with_co2e = {**JSON_INPUT}
    input_with_co2e["logistic"][1]["service"]["CO2ePerKm"] = 1
    input_with_co2e["fuel"][0]["producer"]["CO2ePerKg"] = 1
    logic_input = QueryOutput(**input_with_co2e)
    business_output = BusinessOutput(
        **{
            "fuel": [
                {"type": "TubeTrailer", "amount": 300},
                {"type": "TubeTrailer", "amount": 185},
            ],
            "project": {"location": {"lat": 3, "long": 4.5}},
        }
    )
    logic_layer = LogicLayer()

    logic_output = logic_layer.run(logic_input, business_output)

    # Second only matches as within transport range (110 vs 123 km)
    # fuelUtilisation -> (485 / 600) * 100 = 80.8333333333333
    # price -> (485 * 40) + (111.17 * 40) = 23846.8
    # co2e -> (485 * 1) + (111.17 * 1) = 596.17
    assert json.loads(logic_output.dumps()) == {
        "logistic": [
            {
                "service": {
                    "id": "hydrogen_nrmm:2",
                    "name": "Service 2",
                    "CO2ePerKm": 1,
                },
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
                "price": {"id": "hydrogen_nrmm:2134", "monetaryValue": 40},
            },
        ],
        "fuel": [
            {
                "price": {"id": "hydrogen_nrmm:314", "monetaryValue": 40},
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
                    "CO2ePerKg": 1,
                },
            }
        ],
        "matches": [
            {
                "logistic": "hydrogen_nrmm:2",
                "fuel": "hydrogen_nrmm:3",
                "fuelUtilisation": 80.83,
                "price": 23846.8,
                "transportDistance": 111.17,
                "CO2e": 596.17,
            }
        ],
    }
    with open("tests/schema/SimulationResults.json") as schema:
        exception = False
        try:
            validate(
                instance=json.loads(logic_output.dumps()),
                schema=json.load(schema),
            )
        except Exception as e:
            print(e)
            exception = True
        assert exception == False
