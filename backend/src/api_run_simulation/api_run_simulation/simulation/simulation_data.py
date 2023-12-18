import dataclasses
import json


class SimulationDataJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


class SimulationData:
    def load(self) -> None:
        pass

    def dumps(self) -> str:
        return json.dumps(self.__dict__, cls=SimulationDataJSONEncoder)
