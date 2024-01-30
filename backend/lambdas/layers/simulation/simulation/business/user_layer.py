from simulation import SimulationLayer
from simulation.business import BusinessInput, BusinessOutput
from simulation.business.inputs import Fuel as FuelInput
import simulation.business.outputs as BusinessOutputs


class BusinessLayer(SimulationLayer):
    def run(self, data: BusinessInput) -> BusinessOutput:
        user_output = BusinessOutput(
            self.__fuel_requirements(data.fuel), {"location": data.location.__dict__}
        )

        return user_output

    def __fuel_requirements(self, requirement: FuelInput) -> list[object]:
        tube_trailer_capacity = 300.0
        mcp_capacity = 16.5
        mcp_threshold = 12

        storage_option = BusinessOutputs.Storage.ManifoldCylinderPallet
        capacity = mcp_capacity
        no_storage, partial_fuel = divmod(requirement.amount / capacity, 1)
        if no_storage > mcp_threshold:
            storage_option = BusinessOutputs.Storage.TubeTrailer
            capacity = tube_trailer_capacity
            no_storage, partial_fuel = divmod(requirement.amount / capacity, 1)

        storage_options = list(
            BusinessOutputs.Fuel(storage_option, capacity).__dict__
            for _ in range(0, int(no_storage))
        )

        if partial_fuel > 0:
            storage_options.append(
                BusinessOutputs.Fuel(
                    storage_option,
                    round(capacity * partial_fuel, 2),
                ).__dict__
            )

        return storage_options
