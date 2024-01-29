import { ChakraProvider } from "@chakra-ui/react"
import { render, screen, within } from "@testing-library/react"
import { userEvent } from "@testing-library/user-event"
import * as apiEnvs from "@api/envs"
import * as apiSimulation from "@api/simulation"

import SimulationView from "./SimulationView"

const Latitude = () => screen.getByRole("spinbutton", { name: "Latitude" })
const Longitude = () => screen.getByRole("spinbutton", { name: "Longitude" })
const Amount = () => screen.getByRole("spinbutton", { name: "Amount" })
const Query = () => screen.getByRole("button", { name: "Query testbed" })

const simulationTable = () => screen.getByRole("table", { name: "Simulation results" })

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

    vi.spyOn(apiEnvs, "getAPISimulationURL").mockReturnValue(simulationUrl)
    vi.spyOn(apiEnvs, "getAPISimulationVersion").mockReturnValue(simulationVersion)
    vi.spyOn(apiEnvs, "getAPISimulationRepo").mockReturnValue(simulationRepo)
    vi.spyOn(apiEnvs, "getAPISimulationAccessToken").mockResolvedValue(simulationAccessToken)
  })

  beforeEach(() => {
    simulationAPIMock.mockImplementation(async (data) => {
      simulationAPIMockFn(data)
      return {
        fuel: [{ service: { id: "123", name: "Fuel Service" } }],
        logistic: [{ service: { id: "321", name: "Fuel Logistic" } }],
        matches: [{ fuel: "123", logistic: "321", redundancy: 66 }],
      }
    })
  })

  const renderComponent = () => {
    render(<SimulationView />, { wrapper: ChakraProvider })
  }

  it("shows input form", () => {
    renderComponent()

    expect(Query()).toBeInTheDocument()
    expect(screen.getByRole("heading", { name: "Project site location", level: 5 })).toBeInTheDocument()
    expect(screen.getByRole("heading", { name: "Project fuel requirement", level: 5 })).toBeInTheDocument()
  })

  it("calls API when querying", async () => {
    renderComponent()

    await userEvent.type(Latitude(), "123")
    await userEvent.type(Longitude(), "321")
    await userEvent.type(Amount(), "300")

    await userEvent.click(Query())

    expect(simulationAPIMockFn).toHaveBeenCalledTimes(1)
    expect(simulationAPIMockFn).toHaveBeenCalledWith({ location: { lat: 123, long: 321 }, fuel: { amount: 300 } })
  })

  it("shows simulation results after query", async () => {
    renderComponent()

    await userEvent.type(Latitude(), "123")
    await userEvent.type(Longitude(), "321")
    await userEvent.type(Amount(), "300")

    await userEvent.click(Query())

    const row = rowInTable("Fuel Service")
    expect(row).toBeInTheDocument()
    const rowWithin = within(row)
    rowWithin.getByText("Fuel Logistic")
    rowWithin.getByText("66%")
  })
})
