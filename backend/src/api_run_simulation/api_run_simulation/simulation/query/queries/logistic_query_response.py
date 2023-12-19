from dataclasses import dataclass

from simulation.query.queries import BaseQueryResponse
from simulation.query.queries.hydrogen_nrmm_optional import (
    LogisticService,
    Storage,
    Vehicle,
    DistributionSite,
)


@dataclass
class LogisticQueryResponse(BaseQueryResponse):
    storage: Storage
    service: LogisticService
    vehicle: Vehicle
    distro: DistributionSite
    projectDistance: float

    def __init__(
        self,
        storage: Storage,
        service: LogisticService,
        vehicle: Vehicle,
        distro: DistributionSite,
        projectDistance: float,
    ):
        self.storage = storage
        self.service = service
        self.vehicle = vehicle
        self.distro = distro
        self.projectDistance = projectDistance
