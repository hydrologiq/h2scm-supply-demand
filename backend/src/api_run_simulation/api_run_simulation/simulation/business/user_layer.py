from simulation import SimulationLayer
from simulation.business import BusinessInput, BusinessOutput
from simulation.business.inputs import Fuel as FuelInput
import simulation.business.outputs as BusinessOutputs


class BusinessLayer(SimulationLayer):
    def run(self, data: BusinessInput) -> BusinessOutput:
        user_output = BusinessOutput(
            self.__fuel_requirements(data.fuel), {"location": data.location.__dict__}
        )

        self._done = True

        return user_output

    def __fuel_requirements(self, requirement: FuelInput) -> list[object]:
        tube_trailer_capacity = 300.0
        no_full_trailers, partial_fuel = divmod(
            requirement.amount / tube_trailer_capacity, 1
        )

        trailers = list(
            BusinessOutputs.Fuel(
                BusinessOutputs.Storage.TubeTrailer, tube_trailer_capacity
            ).__dict__
            for _ in range(0, int(no_full_trailers))
        )

        if partial_fuel > 0:
            trailers.append(
                BusinessOutputs.Fuel(
                    BusinessOutputs.Storage.TubeTrailer,
                    tube_trailer_capacity * partial_fuel,
                ).__dict__
            )

        return trailers
