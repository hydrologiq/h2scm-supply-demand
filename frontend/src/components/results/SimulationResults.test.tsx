import { render, screen, within } from "@testing-library/react"
import SimulationResults from "./SimulationResults"
import { Location, SimulationResults as SimulationResultsSchemaType } from "@custom/types/generated/SimulationResults"
import userEvent from "@testing-library/user-event"

const simulationTable = () => screen.getByRole("table", { name: "Simulation results" })
const textInTable = (text: string, withinElement: HTMLElement = simulationTable()) =>
  within(withinElement).getByText(text)
const rowInTable = (text: string, withinElement: HTMLElement = simulationTable()) =>
  within(withinElement).getByRole("row", {
    name: new RegExp(`${text}`),
  })
const popoverIcon = (title: string) => screen.queryByRole("button", { name: title })

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
      console.log(`lat ${position.lat} long ${position.lng}`)
      return <p>{`lat ${position.lat} long ${position.lng}`}</p>
    },
  }
})

describe("simulation output", () => {
  const renderComponent = (
    results: SimulationResultsSchemaType = { fuel: [], logistic: [], matches: [] },
    location: Location = { lat: 2, long: 1 }
  ) => {
    render(<SimulationResults results={results} location={location} />)
  }

  it("shows table", () => {
    renderComponent()

    expect(simulationTable()).toBeInTheDocument()
  })

  it("shows headings", () => {
    renderComponent()

    expect(textInTable("Supply Chain Flow")).toBeInTheDocument()
    expect(textInTable("Weekly metrics")).toBeInTheDocument()
    expect(textInTable("HYDROGEN SOURCE")).toBeInTheDocument()
    expect(textInTable("HYDROGEN PRODUCER > STORAGE PROVIDER > TRANSPORT PROVIDER")).toBeInTheDocument()
    expect(textInTable("CO2e (TONNE)")).toBeInTheDocument()
    expect(textInTable("COST (£)")).toBeInTheDocument()
    expect(textInTable("PRODUCTION CAPACITY USED (%)")).toBeInTheDocument()
  })

  it("shows a single match", () => {
    const results: SimulationResultsSchemaType = {
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
          production: {
            capacity: { weekly: 600, weeklyUsed: 33 },
            method: "SteamMethaneReformingHydrogen",
            location: { lat: 1, long: 2 },
          },
          cost: { total: 33, breakdown: [] },
          transportDistance: 10,
        },
      ],
    }

    renderComponent(results)
    const row = rowInTable("Fuel Service > Storage Rental > Fuel Logistic")
    expect(row).toBeInTheDocument()
    const rowWithin = within(row)
    rowWithin.getByText("Steam Methane Reforming")
    rowWithin.getByText("33.00")
    rowWithin.getByText(`33.00% of 600 kg`)
    rowWithin.getByText("?")
  })

  it("shows match with source", () => {
    const results: SimulationResultsSchemaType = {
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
          production: {
            capacity: { weekly: 600, weeklyUsed: 33 },
            method: "ElectrolyticHydrogen",
            source: "Grid Renewable",
            location: { lat: 1, long: 2 },
          },
          cost: { total: 33, breakdown: [] },
          transportDistance: 10,
        },
      ],
    }

    renderComponent(results)
    const row = rowInTable("Fuel Service > Storage Rental > Fuel Logistic")
    expect(row).toBeInTheDocument()
    const rowWithin = within(row)
    rowWithin.getByText("Electrolytic (Grid Renewable)")
    rowWithin.getByText("33.00")
    rowWithin.getByText("33.00% of 600 kg")
    rowWithin.getByText("?")
  })

  it("shows match with CO2e", () => {
    const results: SimulationResultsSchemaType = {
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
          production: {
            capacity: { weekly: 600, weeklyUsed: 33 },
            method: "SteamMethaneReformingHydrogen",
            location: { lat: 1, long: 2 },
          },
          cost: { total: 33, breakdown: [] },
          transportDistance: 10,
          CO2e: { total: 3300, breakdown: [] },
        },
      ],
    }

    renderComponent(results)
    const row = rowInTable("Fuel Service > Storage Rental > Fuel Logistic")
    expect(row).toBeInTheDocument()
    const rowWithin = within(row)
    rowWithin.getByText("3.30")
  })

  it("shows multiple matches", () => {
    const results: SimulationResultsSchemaType = {
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
          production: {
            capacity: { weekly: 600, weeklyUsed: 66 },
            method: "SteamMethaneReformingHydrogen",
            location: { lat: 1, long: 2 },
          },
          cost: { total: 12, breakdown: [] },
          transportDistance: 123,
        },
        {
          fuel: {
            id: "654",
            name: "Second Fuel",
            exclusiveDownstream: false,
            exclusiveUpstream: false,
            instance: "hydrogen_nrmm:",
          },
          logistic: {
            id: "456",
            name: "Second Fuel Logistic",
            exclusiveDownstream: false,
            exclusiveUpstream: false,
            instance: "hydrogen_nrmm:",
          },
          storage: {
            id: "789",
            name: "Second Storage Rental",
            exclusiveDownstream: false,
            exclusiveUpstream: false,
            instance: "hydrogen_nrmm:",
          },
          production: {
            capacity: { weekly: 600, weeklyUsed: 33 },
            method: "ElectrolyticHydrogen",
            location: { lat: 1, long: 2 },
          },
          cost: { total: 321, breakdown: [] },
          transportDistance: 543,
        },
      ],
    }

    renderComponent(results)
    const row = rowInTable("Fuel Service > Storage Rental > Fuel Logistic")
    expect(row).toBeInTheDocument()
    const rowWithin = within(row)
    rowWithin.getByText("66.00% of 600 kg")
    rowWithin.getByText("12.00")

    const row2 = rowInTable("Second Fuel > Second Storage Rental > Second Fuel Logistic")
    expect(row2).toBeInTheDocument()
    const row2Within = within(row2)
    row2Within.getByText("321.00")
    row2Within.getByText("33.00% of 600 kg")
  })

  describe("popover", () => {
    it("shows popover for cost", async () => {
      const results: SimulationResultsSchemaType = {
        matches: [
          {
            fuel: {
              id: "123",
              name: "Fuel Service",
              exclusiveDownstream: false,
              exclusiveUpstream: false,
              instance: "hydrogen_nrmm",
            },
            logistic: {
              id: "321",
              name: "Fuel Logistic",
              exclusiveDownstream: false,
              exclusiveUpstream: false,
              instance: "hydrogen_nrmm",
            },
            storage: {
              id: "432",
              name: "Storage Rental",
              exclusiveDownstream: false,
              exclusiveUpstream: false,
              instance: "hydrogen_nrmm",
            },
            production: {
              capacity: { weekly: 600, weeklyUsed: 33 },
              method: "SteamMethaneReformingHydrogen",
              location: { lat: 1, long: 2 },
            },
            cost: {
              total: 33,
              breakdown: [{ service: "123", serviceType: "fuel", perUnit: 30, quantity: 2, unit: "kg", value: "GBP" }],
            },
            transportDistance: 10,
          },
        ],
      }

      renderComponent(results)
      const popover = popoverIcon("Row 1 cost breakdown")
      expect(popover).toBeInTheDocument()
      await userEvent.click(popover!)

      const breakdownTable = screen.getByRole("table", { name: "Cost breakdown" })
      expect(textInTable("SERVICE", breakdownTable)).toBeInTheDocument()
      expect(textInTable("QUANTITY", breakdownTable)).toBeInTheDocument()
      expect(textInTable("COST PER UNIT", breakdownTable)).toBeInTheDocument()
      expect(textInTable("TOTAL", breakdownTable)).toBeInTheDocument()
      const row = rowInTable("Fuel Service", breakdownTable)
      expect(row).toBeInTheDocument()
      const rowWithin = within(row)
      rowWithin.getByText("30.00")
      rowWithin.getByText("60.00")
    })

    it("shows popover for CO2e", async () => {
      const results: SimulationResultsSchemaType = {
        matches: [
          {
            fuel: {
              id: "123",
              name: "Fuel Service",
              exclusiveDownstream: false,
              exclusiveUpstream: false,
              instance: "hydrogen_nrmm",
            },
            logistic: {
              id: "321",
              name: "Fuel Logistic",
              exclusiveDownstream: false,
              exclusiveUpstream: false,
              instance: "hydrogen_nrmm",
            },
            storage: {
              id: "432",
              name: "Storage Rental",
              exclusiveDownstream: false,
              exclusiveUpstream: false,
              instance: "hydrogen_nrmm",
            },
            production: {
              capacity: { weekly: 600, weeklyUsed: 33 },
              method: "SteamMethaneReformingHydrogen",
              location: { lat: 1, long: 2 },
            },
            cost: { total: 33, breakdown: [] },
            transportDistance: 10,
            CO2e: {
              total: 1,
              breakdown: [{ service: "123", serviceType: "fuel", perUnit: 15, quantity: 5, unit: "kg", value: "GBP" }],
            },
          },
        ],
      }

      renderComponent(results)
      const popover = popoverIcon("Row 1 CO2e breakdown")
      expect(popover).toBeInTheDocument()
      await userEvent.click(popover!)
      const breakdownTable = screen.getByRole("table", { name: "CO2e breakdown" })

      expect(textInTable("SERVICE", breakdownTable)).toBeInTheDocument()
      expect(textInTable("QUANTITY", breakdownTable)).toBeInTheDocument()
      expect(textInTable("EMISSION PER UNIT", breakdownTable)).toBeInTheDocument()
      expect(textInTable("TOTAL", breakdownTable)).toBeInTheDocument()
      const row = rowInTable("Fuel Service", breakdownTable)
      expect(row).toBeInTheDocument()
      const rowWithin = within(row)
      rowWithin.getByText("15.00")
      rowWithin.getByText("75.00")
    })

    it("shows popover for location", async () => {
      const results: SimulationResultsSchemaType = {
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
            production: {
              capacity: { weekly: 600, weeklyUsed: 33 },
              method: "SteamMethaneReformingHydrogen",
              location: { lat: 1, long: 2 },
            },
            cost: {
              total: 33,
              breakdown: [{ service: "123", serviceType: "fuel", perUnit: 30, quantity: 2, unit: "kg", value: "GBP" }],
            },
            transportDistance: 10,
          },
        ],
      }

      renderComponent(results)
      const popover = popoverIcon("Row 1 location breakdown")
      expect(popover).toBeInTheDocument()
      expect(screen.getByText("lat 2 long 1")).toBeInTheDocument()
      expect(screen.getByText("1 - Project site")).toBeInTheDocument()
      expect(screen.getByText("2 - Fuel Service")).toBeInTheDocument()
    })
  })

  it("toggle on private mode", async () => {
    const results: SimulationResultsSchemaType = {
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
          production: {
            capacity: { weekly: 600, weeklyUsed: 33 },
            method: "SteamMethaneReformingHydrogen",
            location: { lat: 1, long: 2 },
          },
          cost: { total: 33, breakdown: [] },
          transportDistance: 10,
          CO2e: {
            total: 3300,
            breakdown: [{ service: "123", serviceType: "fuel", perUnit: 15, quantity: 5, unit: "kg", value: "GBP" }],
          },
        },
      ],
    }

    renderComponent(results, { lat: 2, long: 1 })

    const settings = popoverIcon("Configure matching supply options")
    expect(settings).toBeInTheDocument()
    await userEvent.click(settings!)
    await userEvent.click(screen.getByRole("checkbox", { name: "Toggle private mode" }))

    const row = rowInTable("Fuel Service > Storage Rental > Fuel Logistic")
    expect(row).toBeInTheDocument()
    const rowWithin = within(row)
    expect(rowWithin.getByText("33.00")).toHaveClass("blur")
    expect(rowWithin.getByText("33.00% of 600 kg")).toHaveClass("blur")
    expect(rowWithin.getByText("3.30")).toHaveClass("blur")
    expect(rowWithin.getAllByText("Fuel Service").at(0)).toHaveClass("blur")
    expect(rowWithin.getByText("Storage Rental")).toHaveClass("blur")
    expect(rowWithin.getByText("Fuel Logistic")).toHaveClass("blur")

    await userEvent.click(popoverIcon("Row 1 CO2e breakdown")!)
    const emisRowWithin = within(rowInTable("Fuel Service", screen.getByRole("table", { name: "CO2e breakdown" })))
    expect(emisRowWithin.getByText("Fuel Service")).toHaveClass("blur")

    await userEvent.click(popoverIcon("Row 1 location breakdown")!)
    expect(screen.getByText("2 - Fuel Service")).toHaveClass("blur")
  })
})
