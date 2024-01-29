import { ChakraProvider } from "@chakra-ui/react"
import { extendTheme } from "@chakra-ui/react"

import "@aws-amplify/ui-react/styles.css"

import { AwsConfigAuth } from "./config/auth"
import { Amplify } from "aws-amplify"
import { Authenticator } from "@aws-amplify/ui-react"
import SimulationView from "@views/SimulationView"
import BodyWrapper from "@components/BodyWrapper"

const breakpoints = {
  base: "0px",
  sm: "320px",
  ms: "480px",
  md: "768px",
  lg: "960px",
  xl: "1200px",
  "2xl": "1536px",
}

const theme = extendTheme({
  fonts: {
    heading: "montserrat",
    body: "montserrat",
    mono: "montserrat",
  },
  breakpoints,
})

Amplify.configure({ Auth: { Cognito: AwsConfigAuth } })
function App() {
  return (
    <Authenticator hideSignUp={true}>
      {() => (
        <ChakraProvider theme={theme}>
          <BodyWrapper>
            <SimulationView />
          </BodyWrapper>
        </ChakraProvider>
      )}
    </Authenticator>
  )
}

export default App
