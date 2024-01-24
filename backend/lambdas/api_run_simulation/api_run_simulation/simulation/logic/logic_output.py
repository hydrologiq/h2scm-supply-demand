from api_run_simulation.simulation.query import QueryOutput
from dataclasses import dataclass

from api_run_simulation.simulation.logic.outputs import Matched


@dataclass
class LogicOutput(QueryOutput):
    matches: list[Matched]
