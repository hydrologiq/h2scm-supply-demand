import { Table, TableCaption, TableContainer, Tbody, Td, Th, Thead, Tr } from "@chakra-ui/react"
import { Breakdown } from "@custom/types/generated/SimulationResults"
import { toFixed } from "@utils/math"
import { toKey } from "@utils/toKey"

export interface SimulationBreakdownProps {
  breakdown: Breakdown[]
  services: Record<string, string>
  caption?: string
  perUnitHeading?: string
  privateMode?: string
}

function SimulationBreakdown({
  breakdown,
  services,
  caption = "breakdown",
  perUnitHeading = "UNIT COST",
  privateMode = "",
}: SimulationBreakdownProps) {
  return (
    <TableContainer marginTop={2}>
      <Table variant="simple">
        <TableCaption>{caption}</TableCaption>
        <Thead>
          <Tr>
            <Th textTransform={"capitalize"} width={"40%"}>
              SERVICE
            </Th>
            <Th textTransform={"capitalize"} isNumeric>
              QUANTITY
            </Th>
            <Th textTransform={"capitalize"} isNumeric>
              {perUnitHeading}
            </Th>
            <Th padding={0}></Th>
            <Th textTransform={"capitalize"} isNumeric>
              TOTAL
            </Th>
            <Th padding={0}></Th>
          </Tr>
        </Thead>
        <Tbody>
          {breakdown &&
            breakdown.map((match) => {
              return (
                <Tr key={toKey(`breakdown-${match.service}-${match.serviceType}`)}>
                  <Td className={privateMode}>{match.service in services ? services[match.service] : "?"}</Td>
                  <Td isNumeric>{toFixed(match.quantity)}</Td>
                  <Td isNumeric className={privateMode}>
                    {toFixed(match.perUnit)}
                  </Td>
                  <Th padding={0}>per {match.unit}</Th>
                  <Td isNumeric className={privateMode}>
                    {toFixed(match.quantity * match.perUnit)}
                  </Td>
                  <Th paddingLeft={0}>{match.value}</Th>
                </Tr>
              )
            })}
        </Tbody>
      </Table>
    </TableContainer>
  )
}

export default SimulationBreakdown
