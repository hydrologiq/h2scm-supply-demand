import SimulationInput, { FormValues } from "@components/input/SimulationInput"
import { simulation } from "@api/simulation"
import { useState } from "react"
import {
  SimulationResults as SimulationResultsSchema,
  Location as SimLocation,
} from "@custom/types/generated/SimulationResults"
import SimulationResults from "@components/results/SimulationResults"
import { Divider, useToast } from "@chakra-ui/react"
import { AxiosError } from "axios"
function SimulationView() {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<SimulationResultsSchema>({ fuel: [], logistic: [], matches: [] })
  const [location, setLocation] = useState<SimLocation>()
  const toast = useToast()

  const onQuery = (data: FormValues) => {
    setLoading(true)
    if ("location" in data) setLocation(data["location"])

    const instances = [...data.query.instance]
    let submitData = structuredClone(data) as Record<string, any>
    delete submitData["query"]
    console.log(instances)
    toast.promise(simulation(submitData, instances), {
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
      <Divider my={5} />
      <SimulationResults loading={loading} results={results} location={location} />
    </>
  )
}

export default SimulationView
