import json
from mock import patch
from simulation.business import (
    BusinessInput,
    BusinessLayer,
)
from simulation.business.outputs import Storage

JSON_INPUT = json.loads(
    """
    {
        "location": {
            "lat": 12.234,
            "long": 43.221
        },
        "fuel": {
            "amount": 485
        }
    }
    """
)

JSON_INPUT_MCP = json.loads(
    """
    {
        "location": {
            "lat": 12.234,
            "long": 43.221
        },
        "fuel": {
            "amount": 170
        }
    }
    """
)

JSON_OUTPUT = json.loads(
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

JSON_OUTPUT_MCP = json.loads(
    """
    {
        "fuel": [
            {
                "type": "ManifoldCylinderPallet",
                "amount": 16.5
            },
            {
                "type": "ManifoldCylinderPallet",
                "amount": 16.5
            },
            {
                "type": "ManifoldCylinderPallet",
                "amount": 16.5
            },
            {
                "type": "ManifoldCylinderPallet",
                "amount": 16.5
            },
            {
                "type": "ManifoldCylinderPallet",
                "amount": 16.5
            },
            {
                "type": "ManifoldCylinderPallet",
                "amount": 16.5
            },
            {
                "type": "ManifoldCylinderPallet",
                "amount": 16.5
            },
            {
                "type": "ManifoldCylinderPallet",
                "amount": 16.5
            },
            {
                "type": "ManifoldCylinderPallet",
                "amount": 16.5
            },
            {
                "type": "ManifoldCylinderPallet",
                "amount": 16.5
            },
            {
                "type": "ManifoldCylinderPallet",
                "amount": 5.0
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


def test_run_user_layer_output():
    user_input = BusinessInput(**JSON_INPUT)
    user_layer = BusinessLayer()

    user_output = user_layer.run(user_input)

    assert user_output.project is not None
    assert user_output.project.location is not None

    assert user_output.project.location.lat == 12.234
    assert user_output.project.location.long == 43.221

    assert len(user_output.fuel) == 2

    fuel1 = user_output.fuel[0]
    assert fuel1.amount == 300
    assert fuel1.type == Storage.TubeTrailer

    fuel2 = user_output.fuel[1]
    assert fuel2.amount == 185
    assert fuel2.type == Storage.TubeTrailer


def test_run_user_layer_dumps():
    user_input = BusinessInput(**JSON_INPUT)
    user_layer = BusinessLayer()

    user_output = user_layer.run(user_input)

    assert json.loads(user_output.dumps()) == JSON_OUTPUT


def test_run_user_layer_mcp_output():
    user_input = BusinessInput(**JSON_INPUT_MCP)
    user_layer = BusinessLayer()

    user_output = user_layer.run(user_input)

    assert json.loads(user_output.dumps()) == JSON_OUTPUT_MCP
