import {
  Table,
  TableCaption,
  TableContainer,
  Tag as ChakraTag,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
  Box,
  Heading,
  GridItem,
  Grid,
  Icon,
  Checkbox,
} from "@chakra-ui/react"
import Popover from "@components/chakra/popover/Popover"
import {
  Instance,
  Match,
  Location as SimLocation,
  SimulationResults as SimulationResultsSchema,
} from "@custom/types/generated/SimulationResults"
import { toKey } from "@utils/toKey"
import SimulationBreakdown from "./SimulationBreakdown"
import { HiOutlineInformationCircle, HiOutlineQuestionMarkCircle } from "react-icons/hi2"
import { toFixed } from "@utils/math"
import { splitHydrogenMethod } from "@utils/string"
import MapPopover from "@components/map/MapPopover"
import { HiOutlineMap } from "react-icons/hi2"
import { useState } from "react"
import { CiSettings } from "react-icons/ci"

interface SimulationResultsProps {
  results: SimulationResultsSchema
  location?: SimLocation
  loading?: boolean
}

const Tag = ({
  children,
  background = true,
  exclusiveUpstream = false,
  exclusiveDownstream = false,
}: {
  children: React.ReactNode
  background?: boolean
  exclusiveUpstream?: boolean
  exclusiveDownstream?: boolean
}) => (
  <ChakraTag
    background={background ? (exclusiveUpstream || exclusiveDownstream ? "purple.100" : "gray.100") : "none"}
    padding={2}
    fontSize={"medium"}
  >
    {children}
  </ChakraTag>
)

const RightTag = () => <Tag background={false}>&gt;</Tag>
const InstanceTag = ({ instance, privateModeClass = "" }: { instance: Instance; privateModeClass?: string }) => (
  <Tag exclusiveDownstream={instance.exclusiveDownstream} exclusiveUpstream={instance.exclusiveUpstream}>
    <span className={privateModeClass}>{instance.name}</span> {instance.instance !== "hydrogen_nrmm:" && " 🔒"}
  </Tag>
)

const ConfigureSectionPopover = ({
  name,
  changeCallback,
}: {
  name: string
  changeCallback: (state: boolean) => void
}): JSX.Element => (
  <Popover icon={<CiSettings />} title={`Configure ${name}`} closeOnBlur={true}>
    <Box pt={2} px={2}>
      <Checkbox onChange={(e) => changeCallback(e.target.checked)}>Toggle private mode</Checkbox>
    </Box>
  </Popover>
)

function SimulationResults({ results, location, loading = false }: SimulationResultsProps) {
  const [selectedRow, setSelectedRow] = useState<number>(-1)
  const allServices: Record<string, string> =
    results !== undefined
      ? results.matches.reduce(
          (obj, match) => ({
            ...obj,
            [match.fuel.id]: match.fuel.name,
            [match.logistic.id]: match.logistic.name,
            [match.storage.id]: match.storage.name,
          }),
          {}
        )
      : {}

  let matches: Match[] = []
  if (!loading && results && results.matches) {
    matches = results.matches.sort((a, b) => (a.cost.total > b.cost.total ? 1 : a.cost.total < b.cost.total ? -1 : 0))
  }
  const [privateMode, setPrivateMode] = useState<boolean>(false)
  const privateClass = privateMode ? "blur" : ""

  return (
    <Box>
      <Box>
        <Heading as={"h2"} size={"lg"}>
          Matching supply options
          <ConfigureSectionPopover
            name="matching supply options"
            changeCallback={(state: boolean) => setPrivateMode(state)}
          />
        </Heading>
        <Grid mt={5}>
          <GridItem>
            <Icon
              mt={1.5}
              mr={1}
              fontSize={"24px"}
              background={"none"}
              aria-label={"Purple tag is a linked service"}
              as={HiOutlineInformationCircle}
            />
            <Tag exclusiveDownstream={true} exclusiveUpstream={true}>
              Purple tag
            </Tag>
            <Tag background={false}>
              indicates it is part of a group of linked services (partner services or vertically integrated services)
            </Tag>
          </GridItem>
          <GridItem>
            <Icon
              mt={1.5}
              mr={1}
              fontSize={"24px"}
              background={"none"}
              aria-label={"Explores the breakdown of a figure"}
              as={HiOutlineQuestionMarkCircle}
            />
            <Tag background={false}>Explores the breakdown of the value to the left of the icon</Tag>
          </GridItem>
          <GridItem>
            <Icon
              mt={1.5}
              mr={1}
              fontSize={"24px"}
              background={"none"}
              aria-label={"Visualises the location of the project site and hydrogen producer"}
              as={HiOutlineMap}
            />
            <Tag background={false}>Visualises the location of the project site and hydrogen producer</Tag>
          </GridItem>
        </Grid>
      </Box>
      <TableContainer marginTop={10}>
        <Table variant="simple">
          <TableCaption>Simulation results</TableCaption>
          <Thead>
            <Tr>
              <Th
                colSpan={3}
                fontSize={"medium"}
                bg="gray.50"
                borderBottom={"solid"}
                borderBottomWidth={"thin"}
                borderBottomColor={"gray.100"}
              >
                Supply Chain Flow
              </Th>
              <Th
                colSpan={10}
                fontSize={"medium"}
                bg="gray.100"
                borderBottom={"solid"}
                borderBottomWidth={"thin"}
                borderBottomColor={"gray.50"}
              >
                Weekly metrics
              </Th>
            </Tr>
            <Tr>
              <Th bg="gray.50" fontSize={"small"} textTransform={"capitalize"}>
                HYDROGEN SOURCE
              </Th>
              <Th bg="gray.50" fontSize={"small"} textTransform={"capitalize"}>
                HYDROGEN PRODUCER &gt; STORAGE PROVIDER &gt; TRANSPORT PROVIDER
              </Th>
              <Th bg="gray.50" />
              <Th bg="gray.100" fontSize={"small"} textTransform={"capitalize"}>
                CO2e (TONNE)
              </Th>
              <Th bg="gray.100" padding={0}></Th>
              <Th bg="gray.100" fontSize={"small"} textTransform={"capitalize"}>
                COST (£)
              </Th>
              <Th bg="gray.100" padding={0}></Th>
              <Th bg="gray.100" fontSize={"small"} textTransform={"capitalize"}>
                PRODUCTION CAPACITY USED (%)
              </Th>
            </Tr>
          </Thead>
          <Tbody>
            {!loading &&
              matches.map((match, index) => {
                const breakdownTitle = (type: string) => `${type} breakdown`
                const breakdownIconTitle = (type: string) => `Row ${index + 1} ${breakdownTitle(type)}`
                return (
                  <Tr
                    background={index == selectedRow ? "gray.100" : "none"}
                    key={toKey(`${match.fuel.id}-${match.storage.id}-${match.logistic.id}`)}
                  >
                    <Td>
                      {splitHydrogenMethod(match.production.method)}
                      {match.production.source && ` (${match.production.source})`}
                    </Td>
                    <Td>
                      <InstanceTag instance={match.fuel} privateModeClass={privateClass} />
                      <RightTag />
                      <InstanceTag instance={match.storage} privateModeClass={privateClass} />
                      <RightTag />
                      <InstanceTag instance={match.logistic} privateModeClass={privateClass} />
                    </Td>
                    <Td padding={0}>
                      <MapPopover
                        title={breakdownIconTitle("location")}
                        onOpen={() => setSelectedRow(index)}
                        onClose={() => setSelectedRow(-1)}
                        focusMarker={location && { title: "Project site", location }}
                        zoom={5}
                        markers={[
                          {
                            location: privateMode ? { lat: 55, long: -361 } : match.production.location,
                            title: match.fuel.name,
                            privateMode: privateClass,
                          },
                        ]}
                      />
                    </Td>
                    <Td isNumeric pr={0} className={privateClass}>
                      {match.CO2e ? toFixed(match.CO2e.total / 1000) : "?"}
                    </Td>
                    <Td padding={0}>
                      {match.CO2e && (
                        <Popover
                          title={breakdownIconTitle("CO2e")}
                          icon={<HiOutlineQuestionMarkCircle />}
                          onOpen={() => setSelectedRow(index)}
                          onClose={() => setSelectedRow(-1)}
                          children={
                            <SimulationBreakdown
                              breakdown={match.CO2e.breakdown}
                              services={allServices}
                              caption={breakdownTitle("CO2e")}
                              perUnitHeading="EMISSION PER UNIT"
                              privateMode={privateClass}
                            />
                          }
                        />
                      )}
                    </Td>
                    <Td isNumeric pr={0} className={privateClass}>
                      {toFixed(match.cost.total)}
                    </Td>
                    <Td padding={0}>
                      <Popover
                        title={breakdownIconTitle("cost")}
                        icon={<HiOutlineQuestionMarkCircle />}
                        onOpen={() => setSelectedRow(index)}
                        onClose={() => setSelectedRow(-1)}
                        children={
                          <SimulationBreakdown
                            breakdown={match.cost.breakdown}
                            services={allServices}
                            caption={breakdownTitle("Cost")}
                            perUnitHeading="COST PER UNIT"
                            privateMode={privateClass}
                          />
                        }
                      />
                    </Td>
                    <Td isNumeric className={privateClass}>{`${toFixed(
                      match.production.capacity.weeklyUsed
                    )}% of ${toFixed(match.production.capacity.weekly, 0)} kg`}</Td>
                  </Tr>
                )
              })}
          </Tbody>
        </Table>
      </TableContainer>
    </Box>
  )
}

export default SimulationResults
