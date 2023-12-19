from dataclasses import dataclass
import dataclasses
import decimal
import json
from simulation.query.queries.hydrogen_nrmm_optional import YAMLRoot


class BaseQueryResponseJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, decimal.Decimal):
            _, p = divmod(o, 1)
            if p > 0:
                return float(o)
            else:
                return int(o)

        return super().default(o)


def clean_nones(value):
    """
    Recursively remove all None values from dictionaries and lists, and returns
    the result as a new dictionary or list.
    """
    if isinstance(value, list):
        return [clean_nones(x) for x in value if x is not None]
    elif isinstance(value, dict):
        return {
            key: clean_nones(val)
            for key, val in value.items()
            if val is not None and not (isinstance(val, list) and len(val) == 0)
        }
    elif isinstance(value, YAMLRoot):
        return clean_nones(value.__dict__)
    else:
        return value


@dataclass
class BaseQueryResponse:
    def dumps(self) -> str:
        return json.dumps(clean_nones(self.__dict__), cls=BaseQueryResponseJSONEncoder)
