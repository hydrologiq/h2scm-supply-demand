from dataclasses import dataclass

from simulation import BaseQueryResponse
from simulation.query.queries.hydrogen_nrmm_optional import (
    LogisticService,
    Quote,
    Vehicle,
    Company,
)


@dataclass
class LogisticQueryResponse(BaseQueryResponse):
    service: LogisticService
    vehicle: Vehicle
    quote: Quote
    company: Company

    def __init__(
        self, service: LogisticService, vehicle: Vehicle, quote: Quote, company: Company
    ):
        self.service = (
            LogisticService(**service)
            if not isinstance(service, LogisticService)
            else service
        )
        self.vehicle = (
            Vehicle(**vehicle) if not isinstance(vehicle, Vehicle) else vehicle
        )
        self.quote = Quote(**quote) if not isinstance(quote, Quote) else quote
        self.company = (
            Company(**company) if not isinstance(company, Company) else company
        )
