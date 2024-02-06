import json
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

JSON_OUTPUT = json.loads(
    """
    {
        "fuel": {
            "total": 485
        },
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

    assert user_output.fuel.total == 485


def test_run_user_layer_dumps():
    user_input = BusinessInput(**JSON_INPUT)
    user_layer = BusinessLayer()

    user_output = user_layer.run(user_input)

    assert json.loads(user_output.dumps()) == JSON_OUTPUT
