# Backend

## Infrastructure

The backend infrastructure can be deployed via AWS and terraform, for more information see the [Infra README](./infra/README.md).

## Lambdas

The backend is ran using AWS Python Lambdas, for more info see [Lambda README](./lambdas/README.md)

## API

The API is hosted in AWS using API Gateway which uses an [OpenAPI spec for deployment](./openapi/SupplyDemandAPI.yml). The [OpenAPI](https://www.openapis.org/) spec is generated as a PDF document which you can find the [latest version here](./openapi/docs/H2SCM_Supply_Demand_API_v1.0.0.pdf).

If you require access to the already hosted API, please file a request through the [API platform page](https://www.hydrologiq.com/api-platform/).
