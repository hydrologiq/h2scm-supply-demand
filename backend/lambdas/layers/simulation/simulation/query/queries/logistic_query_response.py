from dataclasses import dataclass

from simulation import BaseQueryResponse
from simulation.query.queries.hydrogen_nrmm_optional import (
    LogisticService,
    Quote,
    Storage,
    Vehicle,
)


@dataclass
class LogisticQueryResponse(BaseQueryResponse):
    storage: Storage
    service: LogisticService
    vehicle: Vehicle
    quote: Quote

    def __init__(
        self,
        storage: Storage,
        service: LogisticService,
        vehicle: Vehicle,
        quote: Quote,
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
        self.quote = Quote(**quote) if not isinstance(quote, Quote) else quote
