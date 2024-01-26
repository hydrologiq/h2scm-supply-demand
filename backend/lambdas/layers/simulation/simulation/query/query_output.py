from simulation import SimulationData
from dataclasses import dataclass

from simulation.query.queries import (
    LogisticQueryResponse,
    FuelQueryResponse,
)


@dataclass
class QueryOutput(SimulationData):
    logistic: list[LogisticQueryResponse]
    fuel: list[FuelQueryResponse]

    def __post_init__(
        self,
    ):
        self.logistic = [
            LogisticQueryResponse(**logistic_item)
            if not isinstance(logistic_item, LogisticQueryResponse)
            else logistic_item
            for logistic_item in self.logistic
        ]
        self.fuel = [
            FuelQueryResponse(**fuel_item)
            if not isinstance(fuel_item, FuelQueryResponse)
            else fuel_item
            for fuel_item in self.fuel
        ]
