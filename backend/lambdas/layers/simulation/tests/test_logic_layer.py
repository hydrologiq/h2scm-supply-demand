import copy
import json

from jsonschema import validate
from simulation.business import BusinessOutput
from simulation.logic import LogicLayer
from simulation.query import QueryOutput
from tests.helpers.fuel import FuelResponse
import simulation.business.outputs as BusinessOutputs
from tests.helpers.storage import StorageResponse

JSON_INPUT = json.loads(
    """
    {
      "logistic": [
        {
          "company": {"id": "hydrogen_nrmm:15"},
          "service": { "id": "hydrogen_nrmm:1", "name": "Service 1" },
          "vehicle": { "id": "hydrogen_nrmm:123", "name": "Vehicle 1", "availableQuantity": 1, "transportDistance": 110 },
          "quote": { "id": "hydrogen_nrmm:12345", "monetaryValuePerUnit": 80, "unit": "trip", "currency": "GBP"},
          "instance": "hydrogen_nrmm:"
        },
        {
          "company": {"id": "hydrogen_nrmm:25"},
          "service": { "id": "hydrogen_nrmm:2", "name": "Service 2" },
          "vehicle": { "id": "hydrogen_nrmm:212", "name": "Vehicle 2", "availableQuantity": 2, "transportDistance": 123 },
          "quote": { "id": "hydrogen_nrmm:2134", "monetaryValuePerUnit": 40, "unit": "trip", "currency": "GBP"},
          "instance": "hydrogen_nrmm:"
        }
      ],
      "fuel": [
        {
          "company": {"id": "hydrogen_nrmm:315"},
          "quote": { "id": "hydrogen_nrmm:314", "monetaryValuePerUnit": 40, "unit": "kg", "currency": "GBP"},
          "service": { "id": "hydrogen_nrmm:3", "name": "Fuel Service 1" },
          "dispenser": { "id": "hydrogen_nrmm:31", "name": "Dispensing Site 1", "lat": 3, "long": 4 },
          "producer": { "id": "hydrogen_nrmm:312", "name": "Hydrogen Producer 1", "weeklyProductionCapacity": 600 },
          "instance": "hydrogen_nrmm:"
        }
      ],
      "storageRental": [
        {
          "company": {"id": "hydrogen_nrmm:415"},
          "service": { "id": "hydrogen_nrmm:4", "name": "Service 3" },
          "storage": { "id": "hydrogen_nrmm:412", "name": "Tube Trailer", "availableQuantity": 2, "capacity": 300, "type": "hydrogen_nrmm:TubeTrailer" },
          "quote": { "id": "hydrogen_nrmm:413", "monetaryValuePerUnit": 100, "unit": "week", "currency": "GBP"},
          "instance": "hydrogen_nrmm:"
        }
      ]
    }
    """
)


def test_run_logic_layer_output_standard():
    query_input = copy.deepcopy(JSON_INPUT)
    logic_input = QueryOutput(**query_input)
    business_output = BusinessOutput(
        **{
            "fuel": {"total": 485},
            "project": {"location": {"lat": 3, "long": 4.5}},
        }
    )
    logic_layer = LogicLayer()

    logic_output = logic_layer.run(logic_input, business_output)

    # Second only matches as within transport range (110 vs 123 km)
    # (fuel quantity * price per kg) + transport quote + (storage cost * quantity)
    assert json.loads(logic_output.dumps()) == {
        **(query_input),
        "matches": [
            {
                "logistic": {
                    "id": "hydrogen_nrmm:2",
                    "name": "Service 2",
                    "exclusiveDownstream": False,
                    "exclusiveUpstream": False,
                    "instance": "hydrogen_nrmm:",
                },
                "fuel": {
                    "id": "hydrogen_nrmm:3",
                    "name": "Fuel Service 1",
                    "exclusiveDownstream": False,
                    "exclusiveUpstream": False,
                    "instance": "hydrogen_nrmm:",
                },
                "storage": {
                    "id": "hydrogen_nrmm:4",
                    "name": "Service 3",
                    "exclusiveDownstream": False,
                    "exclusiveUpstream": False,
                    "type": "TubeTrailer",
                    "instance": "hydrogen_nrmm:",
                },
                "cost": {
                    "total": 19640,
                    "breakdown": [
                        {
                            "serviceType": "fuel",
                            "service": "hydrogen_nrmm:3",
                            "quantity": 485,
                            "perUnit": 40,
                            "unit": "kg",
                            "value": "GBP",
                        },
                        {
                            "serviceType": "storageRental",
                            "service": "hydrogen_nrmm:4",
                            "quantity": 2,
                            "perUnit": 100,
                            "unit": "week",
                            "value": "GBP",
                        },
                        {
                            "serviceType": "logistic",
                            "service": "hydrogen_nrmm:2",
                            "quantity": 1,
                            "perUnit": 40,
                            "unit": "trip",
                            "value": "GBP",
                        },
                    ],
                },
                "production": {
                    "capacity": {"weekly": 600, "weeklyUsed": 80.83},
                    "method": "Hydrogen",
                    "location": {"lat": 3, "long": 4},
                },
                "transportDistance": 111.17,
            }
        ],
    }


def test_run_logic_layer_output_standard_breakdown_order():
    query_input = copy.deepcopy(JSON_INPUT)
    logic_input = QueryOutput(**query_input)
    business_output = BusinessOutput(
        **{
            "fuel": {"total": 485},
            "project": {"location": {"lat": 3, "long": 4.5}},
        }
    )
    logic_layer = LogicLayer()

    logic_output = logic_layer.run(logic_input, business_output)

    # Second only matches as within transport range (110 vs 123 km)
    # (fuel quantity * price per kg) + transport quote + (storage cost * quantity)
    matches = json.loads(logic_output.dumps())["matches"]
    assert len(matches) == 1
    breakdown = matches[0]["cost"]["breakdown"]
    assert len(breakdown) == 3
    assert breakdown[0]["serviceType"] == "fuel"
    assert breakdown[1]["serviceType"] == "storageRental"
    assert breakdown[2]["serviceType"] == "logistic"


def test_run_logic_layer_output_with_co2e():
    input_with_co2e = copy.deepcopy(JSON_INPUT)
    input_with_co2e["logistic"][0]["vehicle"]["availableQuantity"] = 0
    input_with_co2e["logistic"][1]["service"]["transportCO2e"] = 1
    input_with_co2e["fuel"][0]["producer"]["productionCO2e"] = 1
    logic_input = QueryOutput(**input_with_co2e)
    business_output = BusinessOutput(
        **{
            "fuel": {"total": 485},
            "project": {"location": {"lat": 3, "long": 4.5}},
        }
    )
    logic_layer = LogicLayer()

    logic_output = logic_layer.run(logic_input, business_output)
    del input_with_co2e["logistic"][0]
    # Second only matches as within transport range (110 vs 123 km)
    # co2e -> (485 * 1) + (111.17 * 1) = 596.17
    assert json.loads(logic_output.dumps()) == {
        **(input_with_co2e),
        "matches": [
            {
                "logistic": {
                    "id": "hydrogen_nrmm:2",
                    "name": "Service 2",
                    "exclusiveDownstream": False,
                    "exclusiveUpstream": False,
                    "instance": "hydrogen_nrmm:",
                },
                "fuel": {
                    "id": "hydrogen_nrmm:3",
                    "name": "Fuel Service 1",
                    "exclusiveDownstream": False,
                    "exclusiveUpstream": False,
                    "instance": "hydrogen_nrmm:",
                },
                "storage": {
                    "id": "hydrogen_nrmm:4",
                    "name": "Service 3",
                    "exclusiveDownstream": False,
                    "exclusiveUpstream": False,
                    "type": "TubeTrailer",
                    "instance": "hydrogen_nrmm:",
                },
                "cost": {
                    "total": 19640.0,
                    "breakdown": [
                        {
                            "serviceType": "fuel",
                            "service": "hydrogen_nrmm:3",
                            "quantity": 485.0,
                            "perUnit": 40.0,
                            "unit": "kg",
                            "value": "GBP",
                        },
                        {
                            "serviceType": "storageRental",
                            "service": "hydrogen_nrmm:4",
                            "quantity": 2.0,
                            "perUnit": 100.0,
                            "unit": "week",
                            "value": "GBP",
                        },
                        {
                            "serviceType": "logistic",
                            "service": "hydrogen_nrmm:2",
                            "quantity": 1.0,
                            "perUnit": 40.0,
                            "unit": "trip",
                            "value": "GBP",
                        },
                    ],
                },
                "production": {
                    "capacity": {"weekly": 600, "weeklyUsed": 80.83},
                    "method": "Hydrogen",
                    "location": {"lat": 3, "long": 4},
                },
                "transportDistance": 111.17,
                "CO2e": {
                    "total": 596.17,
                    "breakdown": [
                        {
                            "serviceType": "fuel",
                            "service": "hydrogen_nrmm:3",
                            "quantity": 485.0,
                            "perUnit": 1.0,
                            "unit": "kg",
                            "value": "kg",
                        },
                        {
                            "serviceType": "logistic",
                            "service": "hydrogen_nrmm:2",
                            "quantity": 111.17,
                            "perUnit": 1.0,
                            "unit": "km",
                            "value": "kg",
                        },
                    ],
                },
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
          "quote": { "id": "hydrogen_nrmm:12345", "monetaryValuePerUnit": 80, "unit": "trip", "currency": "GBP"},
          "instance": "hydrogen_nrmm:"
        }
      ],
      "storageRental": [
        {
          "company": {"id": "hydrogen_nrmm:45"},
          "service": { "id": "hydrogen_nrmm:4", "name": "Service 3" },
          "storage": { "id": "hydrogen_nrmm:412", "name": "MCP 123", "availableQuantity": 100, "capacity": 6, "type": "hydrogen_nrmm:ManifoldCylinderPallet" },
          "quote": { "id": "hydrogen_nrmm:413", "monetaryValuePerUnit": 100, "unit": "week", "currency": "GBP"},
          "instance": "hydrogen_nrmm:"
        },
        {
          "company": {"id": "hydrogen_nrmm:55"},
          "service": { "id": "hydrogen_nrmm:5", "name": "Service 4", "exclusiveDownstreamCompanies": ["hydrogen_nrmm:10"] },
          "storage": { "id": "hydrogen_nrmm:512", "name": "Tube Trailer", "availableQuantity": 2, "capacity": 600, "type": "hydrogen_nrmm:TubeTrailer" },
          "quote": { "id": "hydrogen_nrmm:513", "monetaryValuePerUnit": 100, "unit": "week", "currency": "GBP"},
          "instance": "hydrogen_nrmm:"
        }
      ],
        "fuel": [
        {
          "company": {"id": "hydrogen_nrmm:315"},  
          "quote": { "id": "hydrogen_nrmm:314", "monetaryValuePerUnit": 40, "unit": "kg", "currency": "GBP"},
          "service": { "id": "hydrogen_nrmm:3", "name": "Fuel Service 1", "exclusiveDownstreamCompanies": ["hydrogen_nrmm:45"] },
          "dispenser": { "id": "hydrogen_nrmm:31", "name": "Dispensing Site 1", "lat": 3, "long": 4 },
          "producer": { "id": "hydrogen_nrmm:312", "name": "Hydrogen Producer 1", "weeklyProductionCapacity": 600 },
          "instance": "hydrogen_nrmm:"
        },
        {      
          "company": {"id": "hydrogen_nrmm:615"},    
          "quote": { "id": "hydrogen_nrmm:614", "monetaryValuePerUnit": 40, "unit": "kg", "currency": "GBP"},
          "service": { "id": "hydrogen_nrmm:6", "name": "Fuel Service 2", "exclusiveDownstreamCompanies": ["hydrogen_nrmm:55"] },
          "dispenser": { "id": "hydrogen_nrmm:61", "name": "Dispensing Site 2", "lat": 3, "long": 4 },
          "producer": { "id": "hydrogen_nrmm:612", "name": "Hydrogen Producer 2", "weeklyProductionCapacity": 600 },
          "instance": "hydrogen_nrmm:"
        }
      ]
    }
    """
)


def test_run_logic_layer_output_downstream_exclusivity():
    logic_input = QueryOutput(**JSON_INPUT_EXCLUSIVE_DOWNSTREAM)
    business_output = BusinessOutput(
        **{
            "fuel": {"total": 485},
            "project": {"location": {"lat": 3, "long": 4.5}},
        }
    )
    logic_layer = LogicLayer()

    logic_output = logic_layer.run(logic_input, business_output)

    # first only matches due to exclusivity requirements
    # price -> (485 * 40) + 80 + (100 * 81) = 19400 + 80 + 8100 = 27580
    # (fuel quantity * price per kg) + transport quote + (storage cost * quantity)
    assert json.loads(logic_output.dumps()) == {
        **(JSON_INPUT_EXCLUSIVE_DOWNSTREAM),
        "matches": [
            {
                "logistic": {
                    "id": "hydrogen_nrmm:1",
                    "name": "Service 1",
                    "exclusiveDownstream": False,
                    "exclusiveUpstream": False,
                    "instance": "hydrogen_nrmm:",
                },
                "fuel": {
                    "id": "hydrogen_nrmm:3",
                    "name": "Fuel Service 1",
                    "exclusiveDownstream": True,
                    "exclusiveUpstream": False,
                    "instance": "hydrogen_nrmm:",
                },
                "storage": {
                    "id": "hydrogen_nrmm:4",
                    "name": "Service 3",
                    "exclusiveDownstream": False,
                    "exclusiveUpstream": False,
                    "type": "ManifoldCylinderPallet",
                    "instance": "hydrogen_nrmm:",
                },
                "cost": {
                    "total": 27580.0,
                    "breakdown": [
                        {
                            "serviceType": "fuel",
                            "service": "hydrogen_nrmm:3",
                            "quantity": 485.0,
                            "perUnit": 40.0,
                            "unit": "kg",
                            "value": "GBP",
                        },
                        {
                            "serviceType": "storageRental",
                            "service": "hydrogen_nrmm:4",
                            "quantity": 81.0,
                            "perUnit": 100.0,
                            "unit": "week",
                            "value": "GBP",
                        },
                        {
                            "serviceType": "logistic",
                            "service": "hydrogen_nrmm:1",
                            "quantity": 1.0,
                            "perUnit": 80.0,
                            "unit": "trip",
                            "value": "GBP",
                        },
                    ],
                },
                "production": {
                    "capacity": {"weekly": 600, "weeklyUsed": 80.83},
                    "method": "Hydrogen",
                    "location": {"lat": 3, "long": 4},
                },
                "transportDistance": 111.17,
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
          "quote": { "id": "hydrogen_nrmm:12345", "monetaryValuePerUnit": 80, "unit": "trip", "currency": "GBP"},
          "instance": "hydrogen_nrmm:"
        }
      ]
    }
    """
)

STORAGE_RESPONSE_1 = StorageResponse(
    storage="412",
    storageName="Tube Trailer",
    storageAvailableQuantity=2,
    storageCapacity=600,
    service="4",
    serviceName="Service 3",
    serviceExclusiveUpstreamCompanies="315",
    quote="413",
    quoteMonetaryValuePerUnit=100,
    quoteCurrency="GBP",
    quoteUnit="week",
    storageType=BusinessOutputs.Storage.TubeTrailer,
    company="415",
)

STORAGE_RESPONSE_2 = StorageResponse(
    storage="612",
    storageName="Tube Trailer 2",
    storageAvailableQuantity=2,
    storageCapacity=600,
    service="6",
    serviceName="Service 4",
    serviceExclusiveUpstreamCompanies="515",
    quote="613",
    quoteMonetaryValuePerUnit=100,
    quoteCurrency="GBP",
    quoteUnit="week",
    storageType=BusinessOutputs.Storage.TubeTrailer,
    company="615",
)

FUEL_RESPONSE_1 = FuelResponse(
    company="315",
    quote="314",
    quoteMonetaryValuePerUnit=40,
    quoteUnit="kg",
    quoteCurrency="GBP",
    service="3",
    serviceName="Fuel Service 1",
    dispenser="31",
    dispenserName="Dispensing Site 1",
    dispenserLat=3,
    dispenserLong=4,
    producer="312",
    producerName="Hydrogen Producer 1",
    producerWeeklyProductionCapacity=600,
    producerType=BusinessOutputs.Producer.SteamMethaneReformingHydrogen,
)

FUEL_RESPONSE_2 = FuelResponse(
    company="515",
    quote="514",
    quoteMonetaryValuePerUnit=40,
    quoteUnit="kg",
    quoteCurrency="GBP",
    service="5",
    serviceName="Fuel Service 2",
    serviceExclusiveUpstreamCompanies="15",
    dispenser="51",
    dispenserName="Dispensing Site 2",
    dispenserLat=3,
    dispenserLong=4,
    producer="512",
    producerName="Hydrogen Producer 2",
    producerWeeklyProductionCapacity=600,
    producerType=BusinessOutputs.Producer.ElectrolyticHydrogen,
)


def test_run_logic_layer_output_upstream_exclusivity():
    logic_input = QueryOutput(
        JSON_INPUT_EXCLUSIVE_UPSTREAM["logistic"],
        [FUEL_RESPONSE_1.query_response(), FUEL_RESPONSE_2.query_response()],
        [STORAGE_RESPONSE_1.query_response(), STORAGE_RESPONSE_2.query_response()],
    )
    business_output = BusinessOutput(
        **{
            "fuel": {"total": 485},
            "project": {"location": {"lat": 3, "long": 4.5}},
        }
    )
    logic_layer = LogicLayer()

    logic_output = logic_layer.run(logic_input, business_output)

    assert json.loads(logic_output.dumps())["matches"] == [
        {
            "logistic": {
                "id": "hydrogen_nrmm:1",
                "name": "Service 1",
                "exclusiveDownstream": False,
                "exclusiveUpstream": False,
                "instance": "hydrogen_nrmm:",
            },
            "fuel": {
                "id": "hydrogen_nrmm:3",
                "name": "Fuel Service 1",
                "exclusiveDownstream": False,
                "exclusiveUpstream": False,
                "instance": "hydrogen_nrmm:",
            },
            "storage": {
                "id": "hydrogen_nrmm:4",
                "name": "Service 3",
                "exclusiveDownstream": False,
                "exclusiveUpstream": True,
                "type": "TubeTrailer",
                "instance": "hydrogen_nrmm:",
            },
            "cost": {
                "total": 19580.0,
                "breakdown": [
                    {
                        "serviceType": "fuel",
                        "service": "hydrogen_nrmm:3",
                        "quantity": 485.0,
                        "perUnit": 40.0,
                        "unit": "kg",
                        "value": "GBP",
                    },
                    {
                        "serviceType": "storageRental",
                        "service": "hydrogen_nrmm:4",
                        "quantity": 1.0,
                        "perUnit": 100,
                        "unit": "week",
                        "value": "GBP",
                    },
                    {
                        "serviceType": "logistic",
                        "service": "hydrogen_nrmm:1",
                        "quantity": 1.0,
                        "perUnit": 80.0,
                        "unit": "trip",
                        "value": "GBP",
                    },
                ],
            },
            "production": {
                "capacity": {"weekly": 600, "weeklyUsed": 80.83},
                "method": "SteamMethaneReformingHydrogen",
                "location": {"lat": 3, "long": 4},
            },
            "transportDistance": 111.17,
        },
        {
            "logistic": {
                "id": "hydrogen_nrmm:1",
                "name": "Service 1",
                "exclusiveDownstream": False,
                "exclusiveUpstream": False,
                "instance": "hydrogen_nrmm:",
            },
            "fuel": {
                "id": "hydrogen_nrmm:5",
                "name": "Fuel Service 2",
                "exclusiveDownstream": False,
                "exclusiveUpstream": True,
                "instance": "hydrogen_nrmm:",
            },
            "storage": {
                "id": "hydrogen_nrmm:6",
                "name": "Service 4",
                "exclusiveDownstream": False,
                "exclusiveUpstream": True,
                "type": "TubeTrailer",
                "instance": "hydrogen_nrmm:",
            },
            "cost": {
                "total": 19580.0,
                "breakdown": [
                    {
                        "serviceType": "fuel",
                        "service": "hydrogen_nrmm:5",
                        "quantity": 485.0,
                        "perUnit": 40.0,
                        "unit": "kg",
                        "value": "GBP",
                    },
                    {
                        "serviceType": "storageRental",
                        "service": "hydrogen_nrmm:6",
                        "quantity": 1.0,
                        "perUnit": 100.0,
                        "unit": "week",
                        "value": "GBP",
                    },
                    {
                        "serviceType": "logistic",
                        "service": "hydrogen_nrmm:1",
                        "quantity": 1.0,
                        "perUnit": 80.0,
                        "unit": "trip",
                        "value": "GBP",
                    },
                ],
            },
            "production": {
                "capacity": {"weekly": 600, "weeklyUsed": 80.83},
                "method": "ElectrolyticHydrogen",
                "location": {"lat": 3.0, "long": 4.0},
            },
            "transportDistance": 111.17,
        },
    ]


def test_run_logic_layer_output_stored_in():
    response_1_mcp = copy.deepcopy(FUEL_RESPONSE_1)
    response_1_mcp.producerStoredIn = [BusinessOutputs.Storage.ManifoldCylinderPallet]
    logic_input = QueryOutput(
        JSON_INPUT_EXCLUSIVE_UPSTREAM["logistic"],
        [response_1_mcp.query_response(), FUEL_RESPONSE_2.query_response()],
        [STORAGE_RESPONSE_1.query_response(), STORAGE_RESPONSE_2.query_response()],
    )
    business_output = BusinessOutput(
        **{
            "fuel": {"total": 485},
            "project": {"location": {"lat": 3, "long": 4.5}},
        }
    )
    logic_layer = LogicLayer()

    logic_output = logic_layer.run(logic_input, business_output)

    assert json.loads(logic_output.dumps())["matches"] == [
        {
            "logistic": {
                "id": "hydrogen_nrmm:1",
                "name": "Service 1",
                "exclusiveDownstream": False,
                "exclusiveUpstream": False,
                "instance": "hydrogen_nrmm:",
            },
            "fuel": {
                "id": "hydrogen_nrmm:5",
                "name": "Fuel Service 2",
                "exclusiveDownstream": False,
                "exclusiveUpstream": True,
                "instance": "hydrogen_nrmm:",
            },
            "storage": {
                "id": "hydrogen_nrmm:6",
                "name": "Service 4",
                "exclusiveDownstream": False,
                "exclusiveUpstream": True,
                "type": "TubeTrailer",
                "instance": "hydrogen_nrmm:",
            },
            "cost": {
                "total": 19580.0,
                "breakdown": [
                    {
                        "serviceType": "fuel",
                        "service": "hydrogen_nrmm:5",
                        "quantity": 485.0,
                        "perUnit": 40.0,
                        "unit": "kg",
                        "value": "GBP",
                    },
                    {
                        "serviceType": "storageRental",
                        "service": "hydrogen_nrmm:6",
                        "quantity": 1.0,
                        "perUnit": 100.0,
                        "unit": "week",
                        "value": "GBP",
                    },
                    {
                        "serviceType": "logistic",
                        "service": "hydrogen_nrmm:1",
                        "quantity": 1.0,
                        "perUnit": 80.0,
                        "unit": "trip",
                        "value": "GBP",
                    },
                ],
            },
            "production": {
                "capacity": {"weekly": 600, "weeklyUsed": 80.83},
                "method": "ElectrolyticHydrogen",
                "location": {"lat": 3.0, "long": 4.0},
            },
            "transportDistance": 111.17,
        },
    ]


FUEL_RESPONSE_1_SOURCE = FuelResponse(
    company="315",
    quote="314",
    quoteMonetaryValuePerUnit=40,
    quoteUnit="kg",
    quoteCurrency="GBP",
    service="3",
    serviceName="Fuel Service 1",
    dispenser="31",
    dispenserName="Dispensing Site 1",
    dispenserLat=3,
    dispenserLong=4,
    producer="312",
    producerName="Hydrogen Producer 1",
    producerWeeklyProductionCapacity=600,
    producerType=BusinessOutputs.Producer.ElectrolyticHydrogen,
    producerSource="Grid",
)


def test_run_logic_layer_output_production():
    logic_input = QueryOutput(
        JSON_INPUT_EXCLUSIVE_UPSTREAM["logistic"],
        [FUEL_RESPONSE_1_SOURCE.query_response()],
        JSON_INPUT_EXCLUSIVE_UPSTREAM["storageRental"],
    )
    business_output = BusinessOutput(
        **{
            "fuel": {"total": 485},
            "project": {"location": {"lat": 3, "long": 4.5}},
        }
    )
    logic_layer = LogicLayer()

    logic_output = logic_layer.run(logic_input, business_output)

    assert json.loads(logic_output.dumps())["matches"][0]["production"] == {
        "capacity": {"weekly": 600, "weeklyUsed": 80.83},
        "method": "ElectrolyticHydrogen",
        "source": "Grid",
    }


def test_run_logic_layer_output_production():
    logic_input = QueryOutput(
        JSON_INPUT_EXCLUSIVE_UPSTREAM["logistic"],
        [FUEL_RESPONSE_1_SOURCE.query_response()],
        [STORAGE_RESPONSE_1.query_response(), STORAGE_RESPONSE_2.query_response()],
    )
    business_output = BusinessOutput(
        **{
            "fuel": {"total": 485},
            "project": {"location": {"lat": 3, "long": 4.5}},
        }
    )
    logic_layer = LogicLayer()

    logic_output = logic_layer.run(logic_input, business_output)

    assert json.loads(logic_output.dumps())["matches"][0]["production"] == {
        "capacity": {"weekly": 600, "weeklyUsed": 80.83},
        "method": "ElectrolyticHydrogen",
        "source": "Grid",
        "location": {"lat": 3, "long": 4},
    }
