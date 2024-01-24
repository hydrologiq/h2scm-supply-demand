from simulation import SimulationData
from dataclasses import dataclass

from api_run_simulation.simulation.query.queries import (
    LogisticQueryResponse,
    FuelQueryResponse,
)


@dataclass
class QueryOutput(SimulationData):
    logistic: list[LogisticQueryResponse]
    fuel: list[FuelQueryResponse]

    def __init__(
        self,
        logistic: list[LogisticQueryResponse],
        fuel: list[FuelQueryResponse],
    ):
        self.logistic = [
            LogisticQueryResponse(**logistic_item)
            if not isinstance(logistic_item, LogisticQueryResponse)
            else logistic_item
            for logistic_item in logistic
        ]
        self.fuel = [
            FuelQueryResponse(**fuel_item)
            if not isinstance(fuel_item, FuelQueryResponse)
            else fuel_item
            for fuel_item in fuel
        ]
