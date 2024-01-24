from dataclasses import dataclass

from simulation import BaseQueryResponse
from api_run_simulation.simulation.query.queries.hydrogen_nrmm_optional import (
    FuelService,
    Hydrogen,
    DispensingSite,
)


@dataclass
class FuelQueryResponse(BaseQueryResponse):
    producer: Hydrogen
    service: FuelService
    dispenser: DispensingSite

    def __init__(
        self,
        producer: Hydrogen,
        service: FuelService,
        dispenser: DispensingSite,
    ):
        self.producer = (
            Hydrogen(**producer) if not isinstance(producer, Hydrogen) else producer
        )
        self.service = (
            FuelService(**service) if not isinstance(service, FuelService) else service
        )
        self.dispenser = (
            DispensingSite(**dispenser)
            if not isinstance(dispenser, DispensingSite)
            else dispenser
        )
