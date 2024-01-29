import SimulationInput from "@components/input/SimulationInput"
import { simulation } from "@api/simulation"
import { useState } from "react"
import { SimulationResults as SimulationResultsSchema } from "@custom/types/generated/SimulationResults"
import SimulationResults from "@components/results/SimulationResults"
import { useToast } from "@chakra-ui/react"
import { AxiosError } from "axios"

function SimulationView() {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<SimulationResultsSchema>({ fuel: [], logistic: [], matches: [] })

  const toast = useToast()

  const onQuery = (data: Record<string, any>) => {
    setLoading(true)
    toast.promise(simulation(data), {
      success: (data) => {
        setResults(data)
        setLoading(false)
        return { title: "Loaded results" }
      },
      error: (error: AxiosError) => {
        setLoading(false)
        return { title: "Error", description: error.message }
      },
      loading: { title: "Querying..." },
    })
  }

  return (
    <>
      <SimulationInput queryCallback={onQuery} />

      {!loading && <SimulationResults results={results} />}
    </>
  )
}

export default SimulationView
