from dataclasses import dataclass

from simulation import BaseQueryResponse
from simulation.query.queries.hydrogen_nrmm_optional import (
    Rental,
    Quote,
    Storage,
)


@dataclass
class StorageQueryResponse(BaseQueryResponse):
    service: Rental
    storage: Storage
    quote: Quote

    def __init__(
        self,
        service: Rental,
        storage: Storage,
        quote: Quote,
    ):
        self.storage = (
            Storage(**storage) if not isinstance(storage, Storage) else storage
        )
        self.service = Rental(**service) if not isinstance(service, Rental) else service
        self.quote = Quote(**quote) if not isinstance(quote, Quote) else quote
