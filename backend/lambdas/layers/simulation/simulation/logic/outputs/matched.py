from dataclasses import dataclass
from typing import Optional

from simulation import SimulationData


@dataclass
class MatchedStorage(SimulationData):
    id: str
    type: str


@dataclass
class Matched(SimulationData):
    logistic: str
    fuel: str
    fuelUtilisation: float
    price: float
    transportDistance: float
    storage: MatchedStorage
    CO2e: Optional[float] = None
