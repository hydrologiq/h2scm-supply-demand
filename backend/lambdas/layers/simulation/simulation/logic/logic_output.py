from simulation.query import QueryOutput
from dataclasses import dataclass

from simulation.logic.outputs import Matched


@dataclass
class LogicOutput(QueryOutput):
    matches: list[Matched]
