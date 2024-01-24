from dataclasses import dataclass
from api_run_simulation.simulation.business.outputs.storage import Storage


@dataclass
class Fuel:
    type: Storage
    amount: float

    def __post_init__(self):
        self.type = Storage(self.type)
