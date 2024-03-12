from dataclasses import dataclass

import simulation
from simulation.query.queries import BaseServiceQueryResponse
from simulation.query.queries.hydrogen_nrmm_optional import (
    Company,
    Rental,
    Quote,
    Storage,
)


@dataclass
class StorageQueryResponse(BaseServiceQueryResponse):
    service: Rental
    storage: Storage
    quote: Quote
    company: Company
    instance: str

    def __init__(
        self,
        service: Rental,
        storage: Storage,
        quote: Quote,
        company: Company,
        instance: str,
    ):
        if "type" in storage:
            class_type = getattr(
                simulation.query.queries.hydrogen_nrmm_optional,
                storage["type"].replace("hydrogen_nrmm:", ""),
            )
            del storage["type"]
            self.storage = class_type(**storage)
        else:
            self.storage = (
                Storage(**storage) if not isinstance(storage, Storage) else storage
            )
        self.service = Rental(**service) if not isinstance(service, Rental) else service
        self.quote = Quote(**quote) if not isinstance(quote, Quote) else quote
        self.company = (
            Company(**company) if not isinstance(company, Company) else company
        )
        self.instance = instance
