from simulation.business.outputs import Project, Fuel
from simulation import SimulationData
from dataclasses import dataclass


@dataclass
class BusinessOutput(SimulationData):
    fuel: Fuel
    project: Project

    def __post_init__(self):
        self.project = Project(**self.project)
        self.fuel = Fuel(**self.fuel)

    def total_fuel(self) -> int:
        return int(self.fuel.total)

    ## TODO(AAS): Assuming a single vehicle needed since we are only supporting one refuelling a week
    def required_no_vehicles(self) -> int:
        return 1
