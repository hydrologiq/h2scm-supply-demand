from simulation import SimulationLayer
from simulation.business.outputs.fuel import Fuel
from simulation.business.outputs.project import Project
from simulation.query.queries import (
    QueryConfiguration,
    LogisticQuery,
    LogisticQueryInput,
    FuelQuery,
    FuelQueryInput,
    StorageQuery,
    StorageQueryInput,
)
from simulation.query import QueryInput, QueryOutput


class QueryLayer(SimulationLayer):
    configuration: QueryConfiguration

    def __init__(self, config: QueryConfiguration):
        self.configuration = config

    def run(self, data: QueryInput) -> QueryOutput:
        storage_type = self.__storage_type(data.fuel)
        logistics = LogisticQuery(self.configuration).query(
            LogisticQueryInput(storage_type)
        )
        storageRental = StorageQuery(self.configuration).query(
            StorageQueryInput(data.total_fuel())
        )
        fuels = FuelQuery(self.configuration).query(
            FuelQueryInput(data.total_fuel(), storage_type)
        )

        return QueryOutput(logistics, fuels, storageRental)

    def __storage_type(self, fuel: list[Fuel]):
        if len(fuel) > 0:
            return set([_fuel.type for _fuel in fuel]).pop()
        raise Exception("Failed to find fuel storage type")
