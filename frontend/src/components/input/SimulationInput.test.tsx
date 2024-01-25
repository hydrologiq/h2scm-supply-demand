import { ChakraProvider } from "@chakra-ui/react"
import { render, screen } from "@testing-library/react"
import SimulationInput from "./SimulationInput"

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

  const renderComponent = () => {
    render(<SimulationInput />, { wrapper: ChakraProvider })
  }

  it("shows query button", async () => {
    renderComponent()

    expect(screen.getByRole("button", { name: "Query" })).toBeInTheDocument()
  })

  it("shows expected location fields", async () => {
    renderComponent()

    expect(screen.getByRole("heading", { name: "Location", level: 5 })).toBeInTheDocument()
    expect(screen.getByRole("spinbutton", { name: "Latitude" })).toBeInTheDocument()
    expect(screen.getByRole("spinbutton", { name: "Longitude" })).toBeInTheDocument()
  })

  it("shows expected fuel fields", async () => {
    renderComponent()

    expect(screen.getByRole("heading", { name: "Fuel", level: 5 })).toBeInTheDocument()
    expect(screen.getByRole("spinbutton", { name: "Amount" })).toBeInTheDocument()
  })
})
