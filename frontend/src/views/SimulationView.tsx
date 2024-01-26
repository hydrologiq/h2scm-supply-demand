import SimulationInput from "@components/input/SimulationInput"
import { simulation } from "@api/simulation"
import { useState } from "react"
import { SimulationResults as SimulationResultsSchema } from "@custom/types/generated/SimulationResults"
import SimulationResults from "@components/results/SimulationResults"

function SimulationView() {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<SimulationResultsSchema>({ fuel: [], logistic: [], matches: [] })

  return (
    <>
      <SimulationInput
        queryCallback={(data) => {
          setLoading(true)
          simulation(data)
            .then((data) => setResults(data))
            .finally(() => setLoading(false))
        }}
      />

      {!loading && <SimulationResults results={results} />}
    </>
  )
}

export default SimulationView
