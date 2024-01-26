import json
from mock import patch
from simulation.business import (
    BusinessInput,
    BusinessLayer,
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

    assert len(user_output.fuel) == 2

    fuel1 = user_output.fuel[0]
    assert fuel1.amount == 300
    assert fuel1.type == Storage.TubeTrailer

    fuel2 = user_output.fuel[1]
    assert fuel2.amount == 185
    assert fuel2.type == Storage.TubeTrailer
