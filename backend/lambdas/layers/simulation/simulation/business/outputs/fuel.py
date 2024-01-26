from dataclasses import dataclass
from simulation.business.outputs.storage import Storage


@dataclass
class Fuel:
    type: Storage
    amount: float

    def __post_init__(self):
        self.type = Storage(self.type)
