from simulation import SimulationLayer
from simulation.business.outputs.fuel import Fuel
from simulation.business.outputs.project import Project
from simulation.query.queries import (
    QueryConfiguration,
    LogisticQuery,
    LogisticQueryInput,
    FuelQuery,
    FuelQueryInput,
)
from simulation.query import QueryInput, QueryOutput


class QueryLayer(SimulationLayer):
    configuration: QueryConfiguration

    def __init__(self, config: QueryConfiguration):
        self.configuration = config

    def run(self, data: QueryInput) -> QueryOutput:
        logistics = LogisticQuery(self.configuration).query(
            LogisticQueryInput(self.__storage_type(data.fuel))
        )
        fuels = FuelQuery(self.configuration).query(
            FuelQueryInput(
                data.total_fuel(),
            )
        )

        return QueryOutput(logistics, fuels)

    def __minimum_fuel(self, fuel: list[Fuel]):
        if len(fuel) > 0:
            return min([_fuel.amount for _fuel in fuel])
        raise Exception("Failed to find minimum fuel")

    def __storage_type(self, fuel: list[Fuel]):
        if len(fuel) > 0:
            return set([_fuel.type for _fuel in fuel]).pop()
        raise Exception("Failed to find fuel storage type")
