from simulation import SimulationLayer
from simulation.business.outputs.fuel import Fuel
from simulation.business.outputs.project import Project
from simulation.query.queries import QueryConfiguration
from simulation.logic import (
    LogicInput,
    LogicOutput,
)


class LogicLayer(SimulationLayer):
    configuration: QueryConfiguration

    def __init__(self, config: QueryConfiguration):
        self.configuration = config

    def run(self, data: LogicInput) -> LogicOutput:
        return LogicOutput(**{**data.__dict__, "matches": []})
