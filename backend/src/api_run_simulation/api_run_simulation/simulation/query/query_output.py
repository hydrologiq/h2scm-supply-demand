from simulation import SimulationData
from dataclasses import dataclass

from simulation.query.queries import LogisticQueryResponse, FuelQueryResponse


@dataclass
class QueryOutput(SimulationData):
    logistic: list[LogisticQueryResponse]
    fuel: list[FuelQueryResponse]
