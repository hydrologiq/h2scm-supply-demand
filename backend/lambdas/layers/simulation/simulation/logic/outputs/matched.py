from dataclasses import dataclass
from enum import StrEnum
from typing import Optional

from simulation import SimulationData


@dataclass
class MatchedInstance(SimulationData):
    id: str
    name: str
    exclusiveDownstream: bool
    exclusiveUpstream: bool
    instance: str
    type: Optional[str] = None


class ServiceType(StrEnum):
    logistic = "logistic"
    fuel = "fuel"
    storageRental = "storageRental"


@dataclass
class BreakdownItem(SimulationData):
    serviceType: ServiceType
    service: str
    quantity: float
    perUnit: float
    unit: str
    value: str

    def __post_init__(self):
        if not isinstance(self.perUnit, float):
            self.perUnit = float(self.perUnit)
        if not isinstance(self.quantity, float):
            self.quantity = float(self.quantity)


@dataclass
class Breakdown(SimulationData):
    total: int
    breakdown: list[BreakdownItem]


@dataclass
class Location(SimulationData):
    lat: float
    long: float


@dataclass
class ProductionCapacity(SimulationData):
    weekly: float
    weeklyUsed: float


@dataclass
class Production(SimulationData):
    method: str
    capacity: ProductionCapacity
    location: Location
    source: Optional[str] = None


@dataclass
class Matched(SimulationData):
    logistic: MatchedInstance
    fuel: MatchedInstance
    storage: MatchedInstance
    cost: Breakdown
    production: Production
    transportDistance: float
    CO2e: Optional[Breakdown] = None
