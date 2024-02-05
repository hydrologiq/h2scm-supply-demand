from simulation.query.queries import (
    BaseQuery,
    FuelQueryResponse,
    FuelQueryInput,
)
from simulation.query.queries.hydrogen_nrmm_optional import (
    Hydrogen,
    FuelService,
    DispensingSite,
    Quote,
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
            "quote": Quote,
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
select ?producer ?producerName ?producerDailyOfftakeCapacity ?producerProductionCO2e ?dispenser ?dispenserName ?dispenserLat ?dispenserLong ?dispenserFillingStationCapacity ?dispenserFillRate ?service ?serviceName ?quote ?quoteMonetaryValue
where { 
    ?producer rdfs:label ?producerName ;
                hydrogen_nrmm:dailyOfftakeCapacity ?producerDailyOfftakeCapacity ;
                hydrogen_nrmm:basedAt ?dispenser ;.
    FILTER(?producerDailyOfftakeCapacity >= """
            + f"{config.total_fuel}"
            + """)
    OPTIONAL { ?producer hydrogen_nrmm:productionCO2e ?producerProductionCO2e. }
    ?dispenser rdfs:label ?dispenserName;
                hydrogen_nrmm:lat ?dispenserLat;
                hydrogen_nrmm:long ?dispenserLong;
                hydrogen_nrmm:fillingStationCapacity ?dispenserFillingStationCapacity;
                hydrogen_nrmm:fillRate ?dispenserFillRate;.
    ?service hydrogen_nrmm:includes ?producer ;
                rdfs:label ?serviceName;
    OPTIONAL { ?service hydrogen_nrmm:typicalPricing ?quote;.
                ?quote hydrogen_nrmm:monetaryValue ?quoteMonetaryValue. }
}"""
        )
