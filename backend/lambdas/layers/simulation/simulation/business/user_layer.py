from simulation import SimulationLayer
from simulation.business import BusinessInput, BusinessOutput
from simulation.business.inputs import Fuel as FuelInput
import simulation.business.outputs as BusinessOutputs


class BusinessLayer(SimulationLayer):
    def run(self, data: BusinessInput) -> BusinessOutput:
        user_output = BusinessOutput(
            {"total": data.fuel.amount}, {"location": data.location.__dict__}
        )

        return user_output
