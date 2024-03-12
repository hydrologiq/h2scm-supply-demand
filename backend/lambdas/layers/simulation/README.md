# Simulation layer

This lambda layer is a library which other lambdas can build on-top of. The layer has all the querying and logic needed to run the supply and demand simulation.

## Setup

In order to build this layer there is a dependency on a version of the ontology (currently v4.2.0).

## Structure

The layer loosely follows a domain driven design, with segregated classes for business, logic and query contexts.

- Business context is for all operations related to handling the user input and apply business transformations/logic to said input.
- Query context is used to collect all relevant information needed to run the supply and demand simulation. The data is fetched from the [Hydrogen Supply Chain Testbed](https://www.hydrologiq.com/api-platform/).
- Logic context is where all the supply and demand logic happens, which includes filtering and determining the supply chain matches.

### Queries

There are three 'select' queries to the testbed, each retrieving different supplier information you can find these below.

1. The [Storage query](./simulation/query/queries/storage_query.py#42) which queries attributes relating any storage providers (TubeTrailer and ManifoldCylinderPallet) and relating services who can fulfil the required amount of fuel.
1. The [Logistic query](./simulation/query/queries/logistic_query.py#39) which queries attributes relating any logistic providers and relating services that can provide the storage types returned from the previous query.
1. The [Fuel query](./simulation/query/queries/fuel_query.py#39) which queries attributes relating any fuel producers and relating services that can provide the storage types returned from the original query and fulfil the required amount of fuel.

### Logic

The logic layer first applies some rules to the data returned by the query layer, the only rule applied currently is the [VehicleAvailabilityRule](./simulation/logic/rules/filter/vehicle_availability.py) which filters out logistic instances that can't meet the required number of vehicles (currently hard-coded to 1 as we only support once per week refuelling).

Secondly, and most importantly the matching portion of the logic layer. This is where we take the filtered data and apply matching rules to it, the matching rules are as follows:

1. Matching logistic instances to fuel instances the only condition we match on is the point-to-point transport distance from the project site to the fuel production site location.
1. Matching fuel instances to storage instances the only condition we match on is if the storage instance can off-take the storage type that the fuel instance supports.
1. We now check for service exclusivity both upstream and downstream for all matched instances (Logistic, Storage and Fuel).

Assuming a match, we populate additional data points such as cost and CO2e.
