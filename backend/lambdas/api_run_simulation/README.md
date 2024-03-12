# Simulation API

This is a basic API Gateway lambda handler which uses the simulation lambda layer to run the simulation.

## Authentication

We are using JWT/access token issued via Cognito and passed-through via API Gateway, these access tokens are generated using the [Hydrogen Supply Chain Testbed](https://www.hydrologiq.com/api-platform/). The access token is retrieved and then passed through to the simulation layer where it will be used to authenticate with the h2sct API.
