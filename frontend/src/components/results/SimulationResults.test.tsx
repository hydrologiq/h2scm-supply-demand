import { render, screen, within } from "@testing-library/react"
import SimulationResults from "./SimulationResults"
import { SimulationResults as SimulationResultsSchemaType } from "@custom/types/generated/SimulationResults"

const simulationTable = () => screen.getByRole("table", { name: "Simulation results" })
const textInTable = (text: string) => within(simulationTable()).getByText(text)
const rowInTable = (text: string) =>
  within(simulationTable()).getByRole("row", {
    name: new RegExp(`${text}`),
  })

describe("simulation output", () => {
  const renderComponent = (results: SimulationResultsSchemaType = { fuel: [], logistic: [], matches: [] }) => {
    render(<SimulationResults results={results} />)
  }

  it("shows table", () => {
    renderComponent()

    expect(simulationTable()).toBeInTheDocument()
  })

  it("shows headings", () => {
    renderComponent()

    expect(textInTable("FUEL PRODUCER")).toBeInTheDocument()
    expect(textInTable("FUEL TRANSPORTATION")).toBeInTheDocument()
    expect(textInTable("TOTAL CO2e")).toBeInTheDocument()
    expect(textInTable("TOTAL PRICE (£)")).toBeInTheDocument()
    expect(textInTable("FUEL UTILISATION (%)")).toBeInTheDocument()
  })

  it("shows a single match", () => {
    const results: SimulationResultsSchemaType = {
      fuel: [{ service: { id: "123", name: "Fuel Service" } }],
      logistic: [{ service: { id: "321", name: "Fuel Logistic" } }],
      matches: [{ fuel: "123", logistic: "321", fuelUtilisation: 66, price: 33, transportDistance: 10 }],
    }

    renderComponent(results)
    const row = rowInTable("Fuel Service")
    expect(row).toBeInTheDocument()
    const rowWithin = within(row)
    rowWithin.getByText("Fuel Logistic")
    rowWithin.getByText("33")
    rowWithin.getByText("66")
    rowWithin.getByText("?")
  })

  it("shows match with CO2e", () => {
    const results: SimulationResultsSchemaType = {
      fuel: [{ service: { id: "123", name: "Fuel Service" } }],
      logistic: [{ service: { id: "321", name: "Fuel Logistic" } }],
      matches: [{ fuel: "123", logistic: "321", fuelUtilisation: 66, price: 33, transportDistance: 10, CO2e: 1 }],
    }

    renderComponent(results)
    const row = rowInTable("Fuel Service")
    expect(row).toBeInTheDocument()
    const rowWithin = within(row)
    rowWithin.getByText("1")
  })

  it("shows multiple matches", () => {
    const results: SimulationResultsSchemaType = {
      fuel: [{ service: { id: "123", name: "Fuel Service" } }, { service: { id: "654", name: "Second Fuel" } }],
      logistic: [
        { service: { id: "321", name: "Fuel Logistic" } },
        { service: { id: "456", name: "Second Fuel Logistic" } },
      ],
      matches: [
        { fuel: "123", logistic: "321", fuelUtilisation: 66, price: 123, transportDistance: 10 },
        { fuel: "654", logistic: "456", fuelUtilisation: 33, price: 321, transportDistance: 10 },
      ],
    }

    renderComponent(results)
    const row = rowInTable("Fuel Service")
    expect(row).toBeInTheDocument()
    const rowWithin = within(row)
    rowWithin.getByText("Fuel Logistic")
    rowWithin.getByText("123")
    rowWithin.getByText("66")

    const row2 = rowInTable("Second Fuel")
    expect(row2).toBeInTheDocument()
    const row2Within = within(row2)
    row2Within.getByText("Second Fuel Logistic")
    row2Within.getByText("321")
    row2Within.getByText("33")
  })
})
