from dataclasses import dataclass


@dataclass
class Matched:
    logistic: str
    fuel: str
    fuelUtilisation: float
    price: float
    transportDistance: float
