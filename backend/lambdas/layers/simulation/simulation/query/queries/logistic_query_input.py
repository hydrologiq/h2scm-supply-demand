from dataclasses import dataclass
import simulation.business.outputs as BusinessOutputs


@dataclass
class LogisticQueryInput:
    minStorage: float
    storageType: BusinessOutputs.Storage
