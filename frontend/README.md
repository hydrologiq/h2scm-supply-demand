# H2SCM Supply and Demand Frontend

This is a generic frontend application using [React](https://react.dev/), [Vite](https://vitejs.dev/), [Amplify Auth](https://docs.amplify.aws/javascript/build-a-backend/auth/set-up-auth/) and [ChakraUI](https://chakra-ui.com/).

## Environment variables

In order to run the application you need to populate a `.env` file within this directory. This env file needs to have the following variables set:

- `VITE_AWS_AUTH_REGION` - This should reference the H2SCT Cognito instance and can be requested via the [API platform page](https://www.hydrologiq.com/api-platform/)
- `VITE_AWS_AUTH_USER_POOL_ID` - This should reference the H2SCT Cognito instance and can be requested via the [API platform page](https://www.hydrologiq.com/api-platform/)
- `VITE_AWS_AUTH_USER_POOL_WEB_CLIENT_ID` - This should reference the H2SCT Cognito instance and can be requested via the [API platform page](https://www.hydrologiq.com/api-platform/)
- `VITE_AWS_AUTH_COOKIE_STORAGE_DOMAIN` - This is the cookie storage domain to be used by Amplify Auth, when running locally set this to `localhost`
- `VITE_API_SIMULATION_URL` - This should reference the H2SCT API and can be requested via the [API platform page](https://www.hydrologiq.com/api-platform/)
- `VITE_API_SIMULATION_VERSION` - This should reference the H2SCT API and can be requested via the [API platform page](https://www.hydrologiq.com/api-platform/)
- `VITE_API_SIMULATION_REPO` - This should reference the H2SCT API and can be requested via the [API platform page](https://www.hydrologiq.com/api-platform/)
- `VITE_G_MAPS_API_KEY` - This is an API key for Google Maps, you will need to generate one yourself [see this guide](https://developers.google.com/maps/documentation/javascript/get-api-key)

## Running the app

You can start the app locally by running `yarn dev` and run the test by running `yarn test`.
