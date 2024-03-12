import { IconButton, Popover as ChakraPopover, PopoverContent, PopoverTrigger } from "@chakra-ui/react"

export interface PopoverProps {
  title: string
  children?: React.ReactNode
  icon?: React.ReactElement
  closeOnBlur?: boolean
  closeOnEsc?: boolean
  fontSize?: string
  onClose?: () => void
  onOpen?: () => void
}
import { HiOutlineInformationCircle } from "react-icons/hi2"

function Popover({
  title,
  children,
  icon = <HiOutlineInformationCircle />,
  closeOnBlur = true,
  closeOnEsc = true,
  fontSize = "20px",
  onClose,
  onOpen,
}: PopoverProps) {
  return (
    <ChakraPopover closeOnBlur={closeOnBlur} closeOnEsc={closeOnEsc} placement="top" onClose={onClose} onOpen={onOpen}>
      <PopoverTrigger>
        <IconButton
          fontSize={fontSize}
          background={"none"}
          _hover={{
            cursor: "pointer",
            color: "grey",
          }}
          aria-label={title}
          size="sm"
          icon={icon}
        />
      </PopoverTrigger>
      <PopoverContent width={"100%"}>{children}</PopoverContent>
    </ChakraPopover>
  )
}

export default Popover
