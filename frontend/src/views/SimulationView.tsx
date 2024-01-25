import SimulationInput from "@components/input/SimulationInput"
import { simulation } from "@api/simulation"

function SimulationView() {
  return <SimulationInput queryCallback={(data) => simulation(data)} />
}

export default SimulationView
