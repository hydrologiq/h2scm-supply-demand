import { render, screen } from "@testing-library/react"
import Popover from "./Popover"

const infoIcon = (title: string) => screen.queryByRole("button", { name: title })

describe("monitoring figure", () => {
  const renderComponent = (title: string, children?: React.ReactNode) => {
    render(<Popover title={title} children={children} />)
  }

  it("can click icon and show pop over", () => {
    const popoverTitle = "test prop"
    renderComponent(popoverTitle, <p>hello world</p>)
    expect(infoIcon(popoverTitle)).toBeInTheDocument()
    expect(screen.getByText("hello world")).toBeInTheDocument()
  })
})
