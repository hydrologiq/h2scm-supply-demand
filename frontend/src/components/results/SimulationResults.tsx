import { Table, TableCaption, TableContainer, Tbody, Td, Th, Thead, Tr } from "@chakra-ui/react"
import { Fuel, Logistic, SimulationResults as SimulationResultsSchema } from "@custom/types/generated/SimulationResults"
import { toKey } from "@utils/toKey"

interface SimulationResultsProps {
  results: SimulationResultsSchema
}

const getLogisticInstance = (id: string, logistic: Logistic[]): Logistic | undefined =>
  logistic.find((instance) => instance.service?.id == id)
const getFuelInstance = (id: string, fuel: Fuel[]): Logistic | undefined =>
  fuel.find((instance) => instance.service?.id == id)

function SimulationResults({ results }: SimulationResultsProps) {
  return (
    <TableContainer marginTop={10}>
      <Table variant="simple">
        <TableCaption>Simulation results</TableCaption>
        <Thead>
          <Tr>
            <Th textTransform={"capitalize"} width={"30%"}>
              FUEL PRODUCER
            </Th>
            <Th textTransform={"capitalize"} width={"30%"}>
              FUEL TRANSPORTATION
            </Th>
            <Th textTransform={"capitalize"} width={"20%"} isNumeric>
              TOTAL PRICE (£)
            </Th>
            <Th textTransform={"capitalize"} width={"20%"} isNumeric>
              FUEL UTILISATION (%)
            </Th>
          </Tr>
        </Thead>
        <Tbody>
          {results &&
            results.matches.map((match) => {
              const logisticInstance = match.logistic && getLogisticInstance(match.logistic, results.logistic)
              const fuelInstance = match.fuel && getFuelInstance(match.fuel, results.fuel)

              return (
                fuelInstance &&
                logisticInstance && (
                  <Tr key={toKey(`${match.fuel}-${match.logistic}`)}>
                    <Td>{fuelInstance.service?.name}</Td>
                    <Td>{logisticInstance.service?.name}</Td>
                    <Td isNumeric>{match.price}</Td>
                    <Td isNumeric>{match.fuelUtilisation}</Td>
                  </Tr>
                )
              )
            })}
        </Tbody>
      </Table>
    </TableContainer>
  )
}

export default SimulationResults
