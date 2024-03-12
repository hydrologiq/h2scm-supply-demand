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
    graphs: list[str]

    def __init__(self, config: QueryConfiguration, graphs: list[str] = ["default"]):
        self.configuration = config
        self.graphs = graphs

    def run(self, data: QueryInput) -> QueryOutput:
        storageRental = StorageQuery(self.configuration).query(
            StorageQueryInput(data.total_fuel()), self.graphs
        )
        storage_types = self.__storage_types(storageRental)
        logistics = LogisticQuery(self.configuration).query(
            LogisticQueryInput(storage_types), self.graphs
        )

        fuels = FuelQuery(self.configuration).query(
            FuelQueryInput(data.total_fuel(), storage_types), self.graphs
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
