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

    expect(screen.queryByRole("button", { name: "Query" })).toBeInTheDocument()
  })
})
