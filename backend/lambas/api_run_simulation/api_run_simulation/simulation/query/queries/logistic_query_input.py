from dataclasses import dataclass


@dataclass
class LogisticQueryInput:
    minStorage: float
    lat: float
    long: float
