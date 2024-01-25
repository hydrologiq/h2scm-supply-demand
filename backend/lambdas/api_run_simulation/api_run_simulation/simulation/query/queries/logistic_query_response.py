from dataclasses import dataclass

from api_run_simulation.simulation import BaseQueryResponse
from api_run_simulation.simulation.query.queries.hydrogen_nrmm_optional import (
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
        self.distro = (
            DistributionSite(**distro)
            if not isinstance(distro, DistributionSite)
            else distro
        )
        self.projectDistance = (
            float(projectDistance)
            if not isinstance(projectDistance, float)
            else projectDistance
        )
