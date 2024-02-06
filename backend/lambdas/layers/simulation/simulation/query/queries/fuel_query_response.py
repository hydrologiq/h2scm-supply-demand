from dataclasses import dataclass

from simulation import BaseQueryResponse
from simulation.query.queries.hydrogen_nrmm_optional import (
    FuelService,
    Hydrogen,
    DispensingSite,
    Quote,
    Company,
)


@dataclass
class FuelQueryResponse(BaseQueryResponse):
    producer: Hydrogen
    service: FuelService
    dispenser: DispensingSite
    quote: Quote
    company: Company

    def __init__(
        self,
        producer: Hydrogen,
        service: FuelService,
        dispenser: DispensingSite,
        quote: Quote,
        company: Company,
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
        self.quote = Quote(**quote) if not isinstance(quote, Quote) else quote
        self.company = Quote(**company) if not isinstance(company, Company) else company
