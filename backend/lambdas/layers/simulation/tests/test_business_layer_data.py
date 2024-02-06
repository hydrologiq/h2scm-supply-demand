import json
from simulation.business import (
    BusinessInput,
    BusinessOutput,
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
                "lat": 54.7694958,
                "long": -1.6080544     
            }
        }
    }
    """
)


def test_user_data_input():
    user_input = BusinessInput(**JSON_INPUT)

    assert user_input.fuel.amount == 485
    assert user_input.location.lat == 12.234
    assert user_input.location.long == 43.221


def test_user_data_output():
    user_output = BusinessOutput(**JSON_OUTPUT)

    assert user_output.project is not None
    assert user_output.project.location is not None

    assert user_output.project.location.lat == 54.7694958
    assert user_output.project.location.long == -1.6080544

    assert user_output.fuel.total == 485
