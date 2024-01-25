import { ChakraProvider } from "@chakra-ui/react"
import { render, screen } from "@testing-library/react"
import { userEvent } from "@testing-library/user-event"
import SimulationInput from "./SimulationInput"

const Latitude = () => screen.getByRole("spinbutton", { name: "Latitude" })
const Longitude = () => screen.getByRole("spinbutton", { name: "Longitude" })
const Amount = () => screen.getByRole("spinbutton", { name: "Amount" })
const Query = () => screen.getByRole("button", { name: "Query" })

describe("simulation input", () => {
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
  })

  const renderComponent = (queryCallback: (data: Record<string, any>) => void = () => {}) => {
    render(<SimulationInput queryCallback={queryCallback} />, { wrapper: ChakraProvider })
  }

  it("shows query button", () => {
    renderComponent()

    expect(Query()).toBeInTheDocument()
  })

  it("shows expected location fields", () => {
    renderComponent()

    expect(screen.getByRole("heading", { name: "Location", level: 5 })).toBeInTheDocument()
    expect(Latitude()).toBeInTheDocument()
    expect(Longitude()).toBeInTheDocument()
  })

  it("shows expected fuel fields", () => {
    renderComponent()

    expect(screen.getByRole("heading", { name: "Fuel", level: 5 })).toBeInTheDocument()
    expect(Amount()).toBeInTheDocument()
  })

  it("calls callback on query", async () => {
    const queryCallback = vi.fn()
    renderComponent(queryCallback)

    await userEvent.type(Latitude(), "123")
    await userEvent.type(Longitude(), "321")
    await userEvent.type(Amount(), "300")

    await userEvent.click(Query())

    expect(queryCallback).toHaveBeenCalledTimes(1)
    expect(queryCallback).toHaveBeenCalledWith({ location: { lat: 123, long: "321" }, fuel: { amount: 300 } })
  })
})
