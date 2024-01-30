from dataclasses import dataclass
from typing import Optional

from simulation import SimulationData


@dataclass
class Matched(SimulationData):
    logistic: str
    fuel: str
    fuelUtilisation: float
    price: float
    transportDistance: float
    CO2e: Optional[float] = None
