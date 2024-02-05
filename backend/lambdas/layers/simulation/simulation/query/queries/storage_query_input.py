from dataclasses import dataclass
import simulation.business.outputs as BusinessOutputs


@dataclass
class StorageQueryInput:
    minStorage: float
    storageType: BusinessOutputs.Storage
