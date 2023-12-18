from simulation.simulation_data import SimulationData
from typing import Self


class SimulationLayer:
    _done = False

    def run(self, data: SimulationData) -> SimulationData:
        pass

    def done(self) -> bool:
        return self._done
