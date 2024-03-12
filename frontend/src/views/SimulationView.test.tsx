import { ChakraProvider } from "@chakra-ui/react"
import { render, screen, waitFor, within } from "@testing-library/react"
import { userEvent } from "@testing-library/user-event"
import * as apiEnvs from "@api/envs"
import * as apiSimulation from "@api/simulation"

import SimulationView from "./SimulationView"
import * as Amplify from "aws-amplify/auth/cognito"
vi.mock("aws-amplify/auth/cognito", async () => ({ ...((await vi.importActual("aws-amplify/auth/cognito")) as any) }))

vi.mock("@react-google-maps/api", async () => {
  return {
    //@ts-ignore
    GoogleMap: ({ center }: { center: google.maps.LatLng }) => {
      return <p>{`lat ${center.lat} long ${center.lng}`}</p>
    },
    useJsApiLoader: () => {
      return { isLoaded: true }
    },
    Marker: ({ position }: { position: google.maps.LatLng }) => {
      return <p>{`lat ${position.lat} long ${position.lng}`}</p>
    },
  }
})

const Latitude = () => screen.getByRole("spinbutton", { name: "Latitude" })
const Longitude = () => screen.getByRole("spinbutton", { name: "Longitude" })
const Amount = () => screen.getByRole("spinbutton", { name: "Amount" })
const Query = () => screen.getByRole("button", { name: "Evaluate using testbed" })

const simulationTable = () => screen.getByRole("table", { name: "Simulation results" })
const loading = async () => await waitFor(() => expect(screen.queryByText("Loading...")).not.toBeInTheDocument())

const rowInTable = (text: string) =>
  within(simulationTable()).getByRole("row", {
    name: new RegExp(`${text}`),
  })
describe("simulation view", () => {
  const simulationAPIMock = vi.spyOn(apiSimulation, "simulation")
  let simulationAPIMockFn = vi.fn()
  const simulationUrl = "https://localhost"
  const simulationVersion = "v1"
  const simulationRepo = "test"
  const simulationAccessToken = "123456"

  beforeAll(() => {
    Object.defineProperty(window, "matchMedia", {
      writable: true,
      value: vi.fn().mockImplementation((query) => ({
        matches: false,
        media: query,
        onchange: null,
        addListener: vi.fn(), // Deprecated
        removeListener: vi.fn(), // Deprecated
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
        dispatchEvent: vi.fn(),
      })),
    })
    window.scrollTo = vi.fn().mockImplementation(() => {})

    vi.spyOn(apiEnvs, "getAPISimulationURL").mockReturnValue(simulationUrl)
    vi.spyOn(apiEnvs, "getAPISimulationVersion").mockReturnValue(simulationVersion)
    vi.spyOn(apiEnvs, "getAPISimulationRepo").mockReturnValue(simulationRepo)
    vi.spyOn(apiEnvs, "getAPISimulationAccessToken").mockResolvedValue(simulationAccessToken)
    vi.spyOn(Amplify, "fetchUserAttributes").mockResolvedValue({ "custom:instances": JSON.stringify([]) })
  })

  beforeEach(() => {
    simulationAPIMockFn = vi.fn()
    simulationAPIMock.mockImplementation(async (data, instances) => {
      simulationAPIMockFn(data, instances)
      return {
        matches: [
          {
            fuel: {
              id: "123",
              name: "Fuel Service",
              exclusiveDownstream: false,
              exclusiveUpstream: false,
              instance: "hydrogen_nrmm:",
            },
            logistic: {
              id: "321",
              name: "Fuel Logistic",
              exclusiveDownstream: false,
              exclusiveUpstream: false,
              instance: "hydrogen_nrmm:",
            },
            storage: {
              id: "432",
              name: "Storage Rental",
              exclusiveDownstream: false,
              exclusiveUpstream: false,
              instance: "hydrogen_nrmm:",
            },
            cost: { total: 33, breakdown: [] },
            production: {
              capacity: { weekly: 600, weeklyUsed: 66 },
              method: "SteamMethaneReformingHydrogen",
              location: { lat: 1, long: 2 },
            },
            transportDistance: 10,
            CO2e: { total: 1, breakdown: [] },
          },
        ],
      }
    })
  })

  const renderComponent = async () => {
    render(<SimulationView />, { wrapper: ChakraProvider })
    await loading()
  }

  it("shows input form", async () => {
    await renderComponent()

    expect(Query()).toBeInTheDocument()
    expect(screen.getByRole("heading", { name: "Site location", level: 5 })).toBeInTheDocument()
    expect(screen.getByRole("heading", { name: "Hydrogen", level: 5 })).toBeInTheDocument()
  })

  it("shows loading when querying", async () => {
    simulationAPIMock.mockImplementation(() => new Promise((r) => setTimeout(r, 200)))
    await renderComponent()

    await userEvent.type(Latitude(), "123")
    await userEvent.type(Longitude(), "321")
    await userEvent.type(Amount(), "300")

    await userEvent.click(Query())
    expect(screen.getByText("Querying...")).toBeInTheDocument()

    await waitFor(() => {
      expect(screen.queryByText("Querying...")).not.toBeInTheDocument()
    })

    expect(screen.getByText("Loaded results")).toBeInTheDocument()
  })

  it("calls API when querying", async () => {
    await renderComponent()

    await userEvent.type(Amount(), "300")

    await userEvent.click(Query())

    expect(simulationAPIMockFn).toHaveBeenCalledTimes(1)
    expect(simulationAPIMockFn).toHaveBeenLastCalledWith(
      {
        location: { lat: 54.97101, long: -2.45682 },
        fuel: { amount: 300 },
      },
      ["default"]
    )
  })

  it("shows simulation results after query", async () => {
    await renderComponent()

    await userEvent.type(Latitude(), "123")
    await userEvent.type(Longitude(), "321")
    await userEvent.type(Amount(), "300")

    await userEvent.click(Query())

    const row = rowInTable("Fuel Service > Storage Rental > Fuel Logistic")
    expect(row).toBeInTheDocument()
    const rowWithin = within(row)
    rowWithin.getByText("66.00% of 600 kg")
  })
})
