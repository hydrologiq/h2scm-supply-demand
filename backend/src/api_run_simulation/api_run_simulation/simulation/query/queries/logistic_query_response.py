from dataclasses import dataclass

from simulation.query.queries import BaseQueryResponse
from simulation.query.queries.hydrogen_nrmm_optional import (
    LogisticService,
    Storage,
    Vehicle,
)


@dataclass
class LogisticQueryResponse(BaseQueryResponse):
    storage: Storage
    service: LogisticService
    vehicle: Vehicle
    projectDistance: float

    def __init__(
        self,
        storage: Storage,
        service: LogisticService,
        vehicle: Vehicle,
        projectDistance: float,
    ):
        self.storage = storage
        self.service = service
        self.vehicle = vehicle
        self.projectDistance = projectDistance
