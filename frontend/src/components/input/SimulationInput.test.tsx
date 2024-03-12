import { ChakraProvider } from "@chakra-ui/react"
import { render, screen, waitFor } from "@testing-library/react"
import { userEvent } from "@testing-library/user-event"
import SimulationInput from "./SimulationInput"
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

const loading = async () => await waitFor(() => expect(screen.queryByText("Loading...")).not.toBeInTheDocument())

const Latitude = () => screen.getByRole("spinbutton", { name: "Latitude" })
const Longitude = () => screen.getByRole("spinbutton", { name: "Longitude" })
const Amount = () => screen.getByRole("spinbutton", { name: "Amount" })
const Query = () => screen.getByRole("button", { name: "Evaluate using testbed" })

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

    window.scrollTo = vi.fn().mockImplementation(() => {})
  })

  const fetchUserAttributesMock = vi.spyOn(Amplify, "fetchUserAttributes")
  const renderComponent = async (queryCallback: (data: Record<string, any>) => void = () => {}) => {
    render(<SimulationInput queryCallback={queryCallback} />, { wrapper: ChakraProvider })
    await loading()
  }

  const privateInstance = { name: "1234", id: "4321" }

  beforeEach(() => {
    fetchUserAttributesMock.mockResolvedValue({ "custom:instances": JSON.stringify([privateInstance]) })
  })

  it("shows query button", async () => {
    await renderComponent()

    expect(Query()).toBeInTheDocument()
  })

  it("shows expected location fields", async () => {
    await renderComponent()

    expect(screen.getByRole("heading", { name: "Site location", level: 5 })).toBeInTheDocument()
    expect(Latitude()).toBeInTheDocument()
    expect(Longitude()).toBeInTheDocument()
  })

  it("shows expected fuel fields", async () => {
    await renderComponent()

    expect(screen.getByRole("heading", { name: "Hydrogen", level: 5 })).toBeInTheDocument()
    expect(Amount()).toBeInTheDocument()
  })

  it("calls callback on query", async () => {
    const queryCallback = vi.fn()
    await renderComponent(queryCallback)

    await userEvent.type(Amount(), "300")

    await userEvent.click(Query())

    expect(queryCallback).toHaveBeenCalledTimes(1)
    expect(queryCallback).toHaveBeenCalledWith({
      location: { lat: 54.97101, long: -2.45682 },
      fuel: { amount: 300 },
      query: { instance: ["default"] },
    })
  })

  describe("map", () => {
    it("has default center coords", async () => {
      await renderComponent()

      expect(screen.getByText("lat 54.97101 long -2.45682")).toBeInTheDocument()
      expect(Amount()).toBeInTheDocument()
    })
  })
})
