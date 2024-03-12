import dataclasses
import decimal
import json
from linkml_runtime.utils.yamlutils import YAMLRoot


class SimulationDataJSONEncoder(json.JSONEncoder):
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
            if val is not None
            and not (isinstance(val, list) and len(val) == 0)
            and not key.startswith("_")
        }
    elif (
        isinstance(value, YAMLRoot)
        or isinstance(value, BaseQueryResponse)
        or isinstance(value, SimulationData)
    ):
        return clean_nones(value.__dict__)
    else:
        return value


class SimulationData:
    def load(self) -> None:
        pass

    def post_clean(self, cleaned, just_matches: bool = False) -> dict:
        return cleaned

    def dumps(self, just_matches: bool = False) -> str:
        obj = self.post_clean(clean_nones(self.__dict__), just_matches)
        if just_matches:

            for key in list(obj.keys()):
                if key != "matches":
                    del obj[key]
        return json.dumps(obj, cls=SimulationDataJSONEncoder)


class BaseQueryResponse:

    def dumps(self) -> str:
        return json.dumps(clean_nones(self.__dict__), cls=SimulationDataJSONEncoder)

    def to_object(self) -> object:
        return json.loads(self.dumps())
