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

    # def __init__(
    #     self,
    #     producer: Hydrogen,
    #     service: FuelService,
    #     dispenser: DispensingSite,
    # ):
    #     self.producer = producer
    #     self.service = service
    #     self.dispenser = dispenser
