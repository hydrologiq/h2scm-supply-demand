from dataclasses import dataclass

from simulation.query.queries import BaseServiceQueryResponse
from simulation.query.queries.hydrogen_nrmm_optional import (
    LogisticService,
    Quote,
    Vehicle,
    Company,
)


@dataclass
class LogisticQueryResponse(BaseServiceQueryResponse):
    service: LogisticService
    vehicle: Vehicle
    quote: Quote
    company: Company
    instance: str

    def __init__(
        self,
        service: LogisticService,
        vehicle: Vehicle,
        quote: Quote,
        company: Company,
        instance: str,
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
        self.instance = instance
