from dataclasses import dataclass
import simulation.business.outputs as BusinessOutputs


@dataclass
class FuelQueryInput:
    total_fuel: float
    storage_type: BusinessOutputs.Storage
