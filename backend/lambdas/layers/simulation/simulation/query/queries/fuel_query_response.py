from dataclasses import dataclass

from simulation import BaseQueryResponse
from simulation.query.queries.hydrogen_nrmm_optional import (
    FuelService,
    Hydrogen,
    DispensingSite,
    Price,
)


@dataclass
class FuelQueryResponse(BaseQueryResponse):
    producer: Hydrogen
    service: FuelService
    dispenser: DispensingSite
    price: Price

    def __init__(
        self,
        producer: Hydrogen,
        service: FuelService,
        dispenser: DispensingSite,
        price: Price,
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
        self.price = Price(**price) if not isinstance(price, Price) else price
