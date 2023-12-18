from simulation.business.inputs import Location, Fuel
from simulation import SimulationData
from dataclasses import dataclass


@dataclass
class BusinessInput(SimulationData):
    location: Location
    fuel: Fuel

    def __post_init__(self):
        self.location = Location(**self.location)
        self.fuel = Fuel(**self.fuel)
