from simulation.business.inputs import Location, Fuel
from simulation import SimulationData
from dataclasses import dataclass


@dataclass
class BusinessInput(SimulationData):
    location: Location
    fuel: Fuel

    def __init__(self, location: Location, fuel: Fuel):
        self.location = (
            Location(**location) if not isinstance(location, Location) else location
        )
        self.fuel = Fuel(**fuel) if not isinstance(fuel, Fuel) else fuel
