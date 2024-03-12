import Popover from "@components/chakra/popover/Popover"
import Map, { MapProps } from "./Map"
import { HiOutlineMap } from "react-icons/hi2"

type MapPopoverProps = { fontSize?: string; title?: string; onClose?: () => void; onOpen?: () => void } & MapProps

function MapPopover({
  focusMarker,
  locationChange,
  fontSize = "28px",
  zoom,
  title,
  markers,
  onClose,
  onOpen,
}: MapPopoverProps) {
  return (
    <Popover title={title || "map"} icon={<HiOutlineMap />} fontSize={fontSize} onClose={onClose} onOpen={onOpen}>
      <Map focusMarker={focusMarker} locationChange={locationChange} zoom={zoom} markers={markers} />
    </Popover>
  )
}

export default MapPopover
