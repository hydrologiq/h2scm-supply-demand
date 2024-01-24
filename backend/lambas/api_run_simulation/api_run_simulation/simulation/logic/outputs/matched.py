from dataclasses import dataclass


@dataclass
class Matched:
    logistic: str
    fuel: str
    redundancy: float
