from dataclasses import dataclass

from simulation.query.queries import BaseQueryResponse
from simulation.query.queries.hydrogen_nrmm_optional import (
    FuelService,
    Hydrogen,
    DispensingSite,
)


@dataclass
class FuelQueryResponse(BaseQueryResponse):
    producer: Hydrogen
    service: FuelService
    dispenser: DispensingSite
