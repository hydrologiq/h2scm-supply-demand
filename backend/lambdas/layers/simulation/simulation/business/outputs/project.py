from dataclasses import dataclass
from simulation.business.outputs import Location


@dataclass
class Project:
    location: Location

    def __post_init__(self):
        self.location = Location(**self.location)
