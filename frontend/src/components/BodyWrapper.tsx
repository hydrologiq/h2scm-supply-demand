import { Box, Flex } from "@chakra-ui/react"
import logo from "@assets/hydrologiq_logo.png"

function BodyWrapper({ children }: { children: React.ReactNode }) {
  return (
    <Box height="100vh" bg={"white"} fontFamily="montserrat">
      <Box bg="#39aed2" borderRight="0" w={"100%"} h={"60px"}>
        <Flex h="100%" alignItems="center" mx="2" justifyContent="space-between">
          <img src={logo} style={{ height: 55 }} />
        </Flex>
      </Box>
      <Box pt={"20px"} pb={"20px"} px={"20px"} minH="90vh">
        {children}
      </Box>
    </Box>
  )
}

export default BodyWrapper
