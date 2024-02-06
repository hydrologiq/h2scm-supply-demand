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
    StorageQueryResponse,
)
from simulation.query import QueryInput, QueryOutput
import simulation.business.outputs as BusinessOutputs


class QueryLayer(SimulationLayer):
    configuration: QueryConfiguration

    def __init__(self, config: QueryConfiguration):
        self.configuration = config

    def run(self, data: QueryInput) -> QueryOutput:
        storage_type = self.__storage_type(data.fuel)
        storageRental = StorageQuery(self.configuration).query(
            StorageQueryInput(data.total_fuel())
        )
        storage_types = self.__storage_types(storageRental)
        logistics = LogisticQuery(self.configuration).query(
            LogisticQueryInput(storage_types)
        )

        fuels = FuelQuery(self.configuration).query(
            FuelQueryInput(data.total_fuel(), storage_type)
        )

        return QueryOutput(logistics, fuels, storageRental)

    def __storage_types(self, storage: list[StorageQueryResponse]):
        return list(
            set(
                [
                    BusinessOutputs.Storage(_storage.storage.class_name)
                    for _storage in storage
                ]
            )
        )

    def __storage_type(self, fuel: list[Fuel]):
        if len(fuel) > 0:
            return set([_fuel.type for _fuel in fuel]).pop()
        raise Exception("Failed to find fuel storage type")
