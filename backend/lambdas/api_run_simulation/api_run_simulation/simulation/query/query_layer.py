from simulation import SimulationLayer
from api_run_simulation.simulation.business.outputs.fuel import Fuel
from api_run_simulation.simulation.business.outputs.project import Project
from api_run_simulation.simulation.query.queries import (
    QueryConfiguration,
    LogisticQuery,
    LogisticQueryInput,
    FuelQuery,
    FuelQueryInput,
)
from api_run_simulation.simulation.query import QueryInput, QueryOutput


class QueryLayer(SimulationLayer):
    configuration: QueryConfiguration

    def __init__(self, config: QueryConfiguration):
        self.configuration = config

    def run(self, data: QueryInput) -> QueryOutput:
        logistics = LogisticQuery(self.configuration).query(
            LogisticQueryInput(
                self.__minimum_fuel(data.fuel),
                self.__project_lat(data.project),
                self.__project_long(data.project),
            )
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

    def __project_lat(self, project: Project):
        return project.location.lat

    def __project_long(self, project: Project):
        return project.location.long
