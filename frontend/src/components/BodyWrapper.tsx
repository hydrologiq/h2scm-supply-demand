import { Box, Flex } from "@chakra-ui/react"

function BodyWrapper({ children }: { children: React.ReactNode }) {
  return (
    <Box minH="100vh" bg={"white"} fontFamily="montserrat">
      <Box bg="#39aed2" borderRight="0" w={"100%"} h={"50px"} pos="fixed">
        <Flex h="20" alignItems="center" mx="8" justifyContent="space-between">
          {/* <img src={logo} style={{ height: 45 }} /> */}
        </Flex>
        {/* {linkItems.map((link) => (
          <NavItem key={link.name} icon={link.icon} path={link.path} location={location} mb="1">
            {link.name}
          </NavItem>
        ))} */}
      </Box>
      <Box pt={"60px"} pb={"20px"} px={"20px"} minH="100vh">
        {children}
      </Box>
    </Box>
  )
}

export default BodyWrapper
