import { render, screen, within } from "@testing-library/react"
import SimulationBreakdown from "./SimulationBreakdown"
import { Breakdown } from "@custom/types/generated/SimulationResults"

const simulationTable = (caption: string = "breakdown") => screen.getByRole("table", { name: caption })
const textInTable = (text: string) => within(simulationTable()).getByText(text)
const rowInTable = (text: string, withinElement: HTMLElement = simulationTable()) =>
  within(withinElement).getByRole("row", {
    name: new RegExp(`${text}`),
  })

describe("simulation breakdown", () => {
  const renderComponent = (
    breakdown: Breakdown[] = [],
    services: Record<string, string> = {},
    caption?: string,
    perUnitHeading?: string,
    privateMode: string = ""
  ) => {
    render(
      <SimulationBreakdown
        caption={caption}
        breakdown={breakdown}
        services={services}
        perUnitHeading={perUnitHeading}
        privateMode={privateMode}
      />
    )
  }

  it("shows table", () => {
    renderComponent()

    expect(simulationTable()).toBeInTheDocument()
  })

  it("shows headings", () => {
    renderComponent()

    expect(textInTable("SERVICE")).toBeInTheDocument()
    expect(textInTable("QUANTITY")).toBeInTheDocument()
    expect(textInTable("UNIT COST")).toBeInTheDocument()
    expect(textInTable("TOTAL")).toBeInTheDocument()
  })

  it("shows a single match", () => {
    const services: Record<string, string> = { "hydrogen_nrmm:1": "Test Service" }
    const breakdown: Breakdown[] = [
      { quantity: 2, perUnit: 30, service: "hydrogen_nrmm:1", serviceType: "fuel", unit: "kg", value: "GBP" },
    ]

    renderComponent(breakdown, services)
    const row = rowInTable("Test Service")
    expect(row).toBeInTheDocument()
    const rowWithin = within(row)
    rowWithin.getByText("2.00")
    rowWithin.getByText("30.00")
    rowWithin.getByText("per kg")
    rowWithin.getByText("60.00")
    rowWithin.getByText("GBP")
  })

  it("custom caption and heading", () => {
    const services: Record<string, string> = { "hydrogen_nrmm:1": "Test Service" }
    const breakdown: Breakdown[] = [
      { quantity: 2, perUnit: 30, service: "hydrogen_nrmm:1", serviceType: "fuel", unit: "kg", value: "GBP" },
    ]

    renderComponent(breakdown, services, "test123", "Heading 123")
    const row = rowInTable("Test Service", simulationTable("test123"))
    expect(row).toBeInTheDocument()
    const rowWithin = within(row)
    rowWithin.getByText("2.00")
    rowWithin.getByText("30.00")
    rowWithin.getByText("per kg")
    rowWithin.getByText("60.00")
    rowWithin.getByText("GBP")
    screen.getByText("Heading 123")
  })

  it("private mode enabled", () => {
    const services: Record<string, string> = { "hydrogen_nrmm:1": "Test Service" }
    const breakdown: Breakdown[] = [
      { quantity: 2, perUnit: 30, service: "hydrogen_nrmm:1", serviceType: "fuel", unit: "kg", value: "GBP" },
    ]

    renderComponent(breakdown, services, undefined, undefined, "blur")
    const row = rowInTable("Test Service")
    expect(row).toBeInTheDocument()
    const rowWithin = within(row)
    expect(rowWithin.getByText("2.00")).not.toHaveClass("blur")
    expect(rowWithin.getByText("30.00")).toHaveClass("blur")
    expect(rowWithin.getByText("per kg")).not.toHaveClass("blur")
    expect(rowWithin.getByText("60.00")).toHaveClass("blur")
    expect(rowWithin.getByText("GBP")).not.toHaveClass("blur")
  })
})
