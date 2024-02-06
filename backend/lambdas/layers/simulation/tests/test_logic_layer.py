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
          "company": {"id": "hydrogen_nrmm:15"},
          "service": { "id": "hydrogen_nrmm:1", "name": "Service 1" },
          "vehicle": { "id": "hydrogen_nrmm:123", "name": "Vehicle 1", "availableQuantity": 1, "transportDistance": 110 },
          "quote": { "id": "hydrogen_nrmm:12345", "monetaryValuePerUnit": 80}
        },
        {
          "company": {"id": "hydrogen_nrmm:25"},
          "service": { "id": "hydrogen_nrmm:2", "name": "Service 2" },
          "vehicle": { "id": "hydrogen_nrmm:212", "name": "Vehicle 2", "availableQuantity": 2, "transportDistance": 123 },
          "quote": { "id": "hydrogen_nrmm:2134", "monetaryValuePerUnit": 40}
        }
      ],
      "fuel": [
        {
          "company": {"id": "hydrogen_nrmm:315"},
          "quote": { "id": "hydrogen_nrmm:314", "monetaryValuePerUnit": 40},
          "service": { "id": "hydrogen_nrmm:3", "name": "Fuel Service 1" },
          "dispenser": { "id": "hydrogen_nrmm:31", "name": "Dispensing Site 1", "fillRate": 10, "fillingStationCapacity": 3, "lat": 3, "long": 4 },
          "producer": { "id": "hydrogen_nrmm:312", "name": "Hydrogen Producer 1", "dailyOfftakeCapacity": 600 }
        }
      ],
      "storageRental": [
        {
          "company": {"id": "hydrogen_nrmm:415"},
          "service": { "id": "hydrogen_nrmm:4", "name": "Service 3" },
          "storage": { "id": "hydrogen_nrmm:412", "name": "Tube Trailer", "availableQuantity": 2, "capacity": 300 },
          "quote": { "id": "hydrogen_nrmm:413", "monetaryValuePerUnit": 100}
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
    # price -> (485 * 40) + 40 + (100 * 2) = 19400 + 40 + 200 = 19640
    # (fuel quantity * price per kg) + transport quote + (storage cost * quantity)
    assert json.loads(logic_output.dumps()) == {
        "logistic": [
            {
                "company": {"id": "hydrogen_nrmm:25"},
                "service": {"id": "hydrogen_nrmm:2", "name": "Service 2"},
                "vehicle": {
                    "id": "hydrogen_nrmm:212",
                    "name": "Vehicle 2",
                    "availableQuantity": 2,
                    "transportDistance": 123,
                },
                "quote": {"id": "hydrogen_nrmm:2134", "monetaryValuePerUnit": 40},
            },
        ],
        "fuel": [
            {
                "company": {"id": "hydrogen_nrmm:315"},
                "quote": {"id": "hydrogen_nrmm:314", "monetaryValuePerUnit": 40},
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
        "storageRental": [
            {
                "company": {"id": "hydrogen_nrmm:415"},
                "service": {"id": "hydrogen_nrmm:4", "name": "Service 3"},
                "storage": {
                    "id": "hydrogen_nrmm:412",
                    "name": "Tube Trailer",
                    "availableQuantity": 2,
                    "capacity": 300,
                },
                "quote": {"id": "hydrogen_nrmm:413", "monetaryValuePerUnit": 100},
            }
        ],
        "matches": [
            {
                "logistic": "hydrogen_nrmm:2",
                "fuel": "hydrogen_nrmm:3",
                "fuelUtilisation": 80.83,
                "price": 19640,
                "transportDistance": 111.17,
                "storage": {"id": "hydrogen_nrmm:4", "type": "TubeTrailer"},
            }
        ],
    }


def test_run_logic_layer_output_with_co2e():
    input_with_co2e = {**JSON_INPUT}
    input_with_co2e["logistic"][1]["service"]["transportCO2e"] = 1
    input_with_co2e["fuel"][0]["producer"]["productionCO2e"] = 1
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
    # price -> (485 * 40) + 40 + (100 * 2) = 19400 + 40 + 200 = 19640
    # (fuel quantity * price per kg) + transport quote + (storage cost * quantity)
    # co2e -> (485 * 1) + (111.17 * 1) = 596.17
    assert json.loads(logic_output.dumps()) == {
        "logistic": [
            {
                "company": {"id": "hydrogen_nrmm:25"},
                "service": {
                    "id": "hydrogen_nrmm:2",
                    "name": "Service 2",
                    "transportCO2e": 1,
                },
                "vehicle": {
                    "id": "hydrogen_nrmm:212",
                    "name": "Vehicle 2",
                    "availableQuantity": 2,
                    "transportDistance": 123,
                },
                "quote": {"id": "hydrogen_nrmm:2134", "monetaryValuePerUnit": 40},
            },
        ],
        "fuel": [
            {
                "company": {"id": "hydrogen_nrmm:315"},
                "quote": {"id": "hydrogen_nrmm:314", "monetaryValuePerUnit": 40},
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
                    "productionCO2e": 1,
                },
            }
        ],
        "storageRental": [
            {
                "company": {"id": "hydrogen_nrmm:415"},
                "service": {"id": "hydrogen_nrmm:4", "name": "Service 3"},
                "storage": {
                    "id": "hydrogen_nrmm:412",
                    "name": "Tube Trailer",
                    "availableQuantity": 2,
                    "capacity": 300,
                },
                "quote": {"id": "hydrogen_nrmm:413", "monetaryValuePerUnit": 100},
            }
        ],
        "matches": [
            {
                "logistic": "hydrogen_nrmm:2",
                "fuel": "hydrogen_nrmm:3",
                "fuelUtilisation": 80.83,
                "price": 19640.0,
                "transportDistance": 111.17,
                "CO2e": 596.17,
                "storage": {"id": "hydrogen_nrmm:4", "type": "TubeTrailer"},
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


JSON_INPUT_EXCLUSIVE_DOWNSTREAM = json.loads(
    """
    {
      "logistic": [
        {
          "company": {"id": "hydrogen_nrmm:15"},
          "service": { "id": "hydrogen_nrmm:1", "name": "Service 1" },
          "vehicle": { "id": "hydrogen_nrmm:123", "name": "Vehicle 1", "availableQuantity": 2, "transportDistance": 123 },
          "quote": { "id": "hydrogen_nrmm:12345", "monetaryValuePerUnit": 80}
        }
      ],
      "storageRental": [
        {
          "company": {"id": "hydrogen_nrmm:45"},
          "service": { "id": "hydrogen_nrmm:4", "name": "Service 3" },
          "storage": { "id": "hydrogen_nrmm:412", "name": "MCP 123", "availableQuantity": 100, "capacity": 6 },
          "quote": { "id": "hydrogen_nrmm:413", "monetaryValuePerUnit": 100}
        },
        {
          "company": {"id": "hydrogen_nrmm:55"},
          "service": { "id": "hydrogen_nrmm:5", "name": "Service 4", "exclusiveDownstreamCompanies": ["hydrogen_nrmm:10"] },
          "storage": { "id": "hydrogen_nrmm:512", "name": "Tube Trailer", "availableQuantity": 2, "capacity": 600 },
          "quote": { "id": "hydrogen_nrmm:513", "monetaryValuePerUnit": 100}
        }
      ],
        "fuel": [
        {
          "company": {"id": "hydrogen_nrmm:315"},  
          "quote": { "id": "hydrogen_nrmm:314", "monetaryValuePerUnit": 40},
          "service": { "id": "hydrogen_nrmm:3", "name": "Fuel Service 1", "exclusiveDownstreamCompanies": ["hydrogen_nrmm:45"] },
          "dispenser": { "id": "hydrogen_nrmm:31", "name": "Dispensing Site 1", "fillRate": 10, "fillingStationCapacity": 3, "lat": 3, "long": 4 },
          "producer": { "id": "hydrogen_nrmm:312", "name": "Hydrogen Producer 1", "dailyOfftakeCapacity": 600 }
        },
        {      
          "company": {"id": "hydrogen_nrmm:615"},    
          "quote": { "id": "hydrogen_nrmm:614", "monetaryValuePerUnit": 40},
          "service": { "id": "hydrogen_nrmm:6", "name": "Fuel Service 2", "exclusiveDownstreamCompanies": ["hydrogen_nrmm:55"] },
          "dispenser": { "id": "hydrogen_nrmm:61", "name": "Dispensing Site 2", "fillRate": 10, "fillingStationCapacity": 3, "lat": 3, "long": 4 },
          "producer": { "id": "hydrogen_nrmm:612", "name": "Hydrogen Producer 2", "dailyOfftakeCapacity": 600 }
        }
      ]
    }
    """
)


def test_run_logic_layer_output_downstream_exclusivity():
    logic_input = QueryOutput(**JSON_INPUT_EXCLUSIVE_DOWNSTREAM)
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

    # first only matches due to exclusivity requirements
    # fuelUtilisation -> (485 / 600) * 100 = 80.8333333333333
    # price -> (485 * 40) + 80 + (100 * 81) = 19400 + 80 + 8100 = 27580
    # (fuel quantity * price per kg) + transport quote + (storage cost * quantity)
    assert json.loads(logic_output.dumps()) == {
        **(JSON_INPUT_EXCLUSIVE_DOWNSTREAM),
        "matches": [
            {
                "logistic": "hydrogen_nrmm:1",
                "fuel": "hydrogen_nrmm:3",
                "fuelUtilisation": 80.83,
                "price": 27580.0,
                "transportDistance": 111.17,
                "storage": {"id": "hydrogen_nrmm:4", "type": "TubeTrailer"},
            }
        ],
    }


JSON_INPUT_EXCLUSIVE_UPSTREAM = json.loads(
    """
    {
      "logistic": [
        {
          "company": {"id": "hydrogen_nrmm:15"},
          "service": { "id": "hydrogen_nrmm:1", "name": "Service 1" },
          "vehicle": { "id": "hydrogen_nrmm:123", "name": "Vehicle 1", "availableQuantity": 2, "transportDistance": 123 },
          "quote": { "id": "hydrogen_nrmm:12345", "monetaryValuePerUnit": 80}
        }
      ],
      "fuel": [
        {        
          "company": {"id": "hydrogen_nrmm:315"},  
          "quote": { "id": "hydrogen_nrmm:314", "monetaryValuePerUnit": 40},
          "service": { "id": "hydrogen_nrmm:3", "name": "Fuel Service 1" },
          "dispenser": { "id": "hydrogen_nrmm:31", "name": "Dispensing Site 1", "fillRate": 10, "fillingStationCapacity": 3, "lat": 3, "long": 4 },
          "producer": { "id": "hydrogen_nrmm:312", "name": "Hydrogen Producer 1", "dailyOfftakeCapacity": 600 }
        },
        {       
          "company": {"id": "hydrogen_nrmm:515"},   
          "quote": { "id": "hydrogen_nrmm:514", "monetaryValuePerUnit": 40},
          "service": { "id": "hydrogen_nrmm:5", "name": "Fuel Service 2", "exclusiveUpstreamCompanies": ["hydrogen_nrmm:15"] },
          "dispenser": { "id": "hydrogen_nrmm:51", "name": "Dispensing Site 1", "fillRate": 10, "fillingStationCapacity": 3, "lat": 3, "long": 4 },
          "producer": { "id": "hydrogen_nrmm:512", "name": "Hydrogen Producer 1", "dailyOfftakeCapacity": 600 }
        }
      ],
      "storageRental": [
        {
          "company": {"id": "hydrogen_nrmm:415"},
          "service": { "id": "hydrogen_nrmm:4", "name": "Service 3", "exclusiveUpstreamCompanies": ["hydrogen_nrmm:315"] },
          "storage": { "id": "hydrogen_nrmm:412", "name": "Tube Trailer", "availableQuantity": 2, "capacity": 600 },
          "quote": { "id": "hydrogen_nrmm:413", "monetaryValuePerUnit": 100}
        },
        {
          "company": {"id": "hydrogen_nrmm:615"},
          "service": { "id": "hydrogen_nrmm:6", "name": "Service 4", "exclusiveUpstreamCompanies": ["hydrogen_nrmm:515"] },
          "storage": { "id": "hydrogen_nrmm:612", "name": "Tube Trailer 2", "availableQuantity": 2, "capacity": 600 },
          "quote": { "id": "hydrogen_nrmm:613", "monetaryValuePerUnit": 100}
        }
      ]
    }
    """
)


def test_run_logic_layer_output_upstream_exclusivity():
    logic_input = QueryOutput(**JSON_INPUT_EXCLUSIVE_UPSTREAM)
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

    assert json.loads(logic_output.dumps()) == {
        **(JSON_INPUT_EXCLUSIVE_UPSTREAM),
        "matches": [
            {
                "logistic": "hydrogen_nrmm:1",
                "fuel": "hydrogen_nrmm:3",
                "fuelUtilisation": 80.83,
                "price": 19580.0,
                "transportDistance": 111.17,
                "storage": {"id": "hydrogen_nrmm:4", "type": "TubeTrailer"},
            }
        ],
    }
