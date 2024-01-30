from simulation.query.queries import (
    BaseQuery,
    FuelQueryResponse,
    FuelQueryInput,
)
from simulation.query.queries.hydrogen_nrmm_optional import (
    Hydrogen,
    FuelService,
    DispensingSite,
    Price,
)


class FuelQuery(BaseQuery):
    def query(self, config: FuelQueryInput) -> list[FuelQueryResponse]:
        return super().query(config)

    def _parse_query(self, resp_obj) -> list[FuelQueryResponse]:
        bindings = resp_obj["results"]["bindings"]
        class_types = {
            "producer": Hydrogen,
            "service": FuelService,
            "dispenser": DispensingSite,
            "price": Price,
        }
        matching_instances = self._get_matching_instances(
            bindings,
            class_types.keys(),
        )
        self._convert_matched_instances(matching_instances, class_types)
        return [FuelQueryResponse(**instance) for instance in matching_instances]

    def _get_query(self, config: FuelQueryInput):
        return (
            """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?producer ?producerName ?producerDailyOfftakeCapacity ?producerCO2ePerKg ?dispenser ?dispenserName ?dispenserLat ?dispenserLong ?dispenserFillingStationCapacity ?dispenserFillRate ?service ?serviceName ?price ?priceMonetaryValue
        where { 
            ?producer rdfs:label ?producerName ;
                      hydrogen_nrmm:dailyOfftakeCapacity ?producerDailyOfftakeCapacity ;
                      hydrogen_nrmm:basedAt ?dispenser ;.
            FILTER(?producerDailyOfftakeCapacity >= """
            + f"{config.total_fuel}"
            + """)
            OPTIONAL { ?producer hydrogen_nrmm:CO2ePerKg ?producerCO2ePerKg. }
            ?dispenser rdfs:label ?dispenserName;
                      hydrogen_nrmm:lat ?dispenserLat;
                      hydrogen_nrmm:long ?dispenserLong;
                      hydrogen_nrmm:fillingStationCapacity ?dispenserFillingStationCapacity;
                      hydrogen_nrmm:fillRate ?dispenserFillRate;.
            ?service hydrogen_nrmm:includes ?producer ;
                      rdfs:label ?serviceName;
                      hydrogen_nrmm:typicalPricing ?quote;.
            ?quote hydrogen_nrmm:price ?price;.
            ?price hydrogen_nrmm:monetaryValue ?priceMonetaryValue;
        }
    """
        )
