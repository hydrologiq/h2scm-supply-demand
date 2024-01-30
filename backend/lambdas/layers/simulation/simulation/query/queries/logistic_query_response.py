from dataclasses import dataclass

from simulation import BaseQueryResponse
from simulation.query.queries.hydrogen_nrmm_optional import (
    LogisticService,
    Price,
    Storage,
    Vehicle,
    DistributionSite,
)


@dataclass
class LogisticQueryResponse(BaseQueryResponse):
    storage: Storage
    service: LogisticService
    vehicle: Vehicle
    price: Price

    def __init__(
        self,
        storage: Storage,
        service: LogisticService,
        vehicle: Vehicle,
        price: Price,
    ):
        self.storage = (
            Storage(**storage) if not isinstance(storage, Storage) else storage
        )
        self.service = (
            LogisticService(**service)
            if not isinstance(service, LogisticService)
            else service
        )
        self.vehicle = (
            Vehicle(**vehicle) if not isinstance(vehicle, Vehicle) else vehicle
        )
        self.price = Price(**price) if not isinstance(price, Price) else price
