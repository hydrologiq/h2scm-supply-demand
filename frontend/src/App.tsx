import { ChakraProvider, ThemeProviderProps } from "@chakra-ui/react"
import "./App.css"
import { extendTheme } from "@chakra-ui/react"

const theme = extendTheme({}) as ThemeProviderProps
import "@aws-amplify/ui-react/styles.css"

import { AwsConfigAuth } from "./config/auth"
import { Amplify } from "aws-amplify"
import { Authenticator } from "@aws-amplify/ui-react"
import SimulationInput from "./components/input/SimulationInput"
Amplify.configure({ Auth: { Cognito: AwsConfigAuth } })
function App() {
  return (
    <Authenticator hideSignUp={true}>
      {() => (
        <ChakraProvider theme={theme}>
          <h1>Vite + React</h1>
          <div className="card">
            <p>
              Edit <code>src/App.tsx</code> and save to test HMR
            </p>
          </div>
          <p className="read-the-docs">Click on the Vite and React logos to learn more</p>
          <SimulationInput />
        </ChakraProvider>
      )}
    </Authenticator>
  )
}

export default App
