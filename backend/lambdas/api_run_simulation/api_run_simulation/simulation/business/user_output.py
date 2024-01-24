from api_run_simulation.simulation.business.outputs import Project, Fuel
from simulation import SimulationData
from dataclasses import dataclass


@dataclass
class BusinessOutput(SimulationData):
    fuel: list[Fuel]
    project: Project

    def __post_init__(self):
        self.project = Project(**self.project)
        self.fuel = list(map(lambda r: Fuel(**r), self.fuel))

    def total_fuel(self) -> float:
        return sum([_fuel.amount for _fuel in self.fuel])

    def required_no_vehicles(self) -> int:
        return len(self.fuel)
