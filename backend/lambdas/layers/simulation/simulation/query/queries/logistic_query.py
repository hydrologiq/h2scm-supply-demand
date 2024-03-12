from simulation.query.queries import (
    BaseQuery,
    LogisticQueryResponse,
    LogisticQueryInput,
)
from simulation.query.queries.hydrogen_nrmm_optional import (
    Company,
    Quote,
    LogisticService,
    Vehicle,
)


class LogisticQuery(BaseQuery):
    def query(self, config: LogisticQueryInput, graphs: list[str] = ["default"]) -> list[LogisticQueryResponse]:
        return super().query(config, graphs)

    def _parse_query(self, resp_obj) -> list[LogisticQueryResponse]:
        if "results" not in resp_obj:
            raise Exception(f"Could not query with error -- {resp_obj}")
        bindings = resp_obj["results"]["bindings"]
        class_types = {
            "service": LogisticService,
            "vehicle": Vehicle,
            "quote": Quote,
            "company": Company,
            "instance": str
        }
        matching_instances = self._get_matching_instances(
            bindings,
            class_types.keys(),
        )
        self._convert_matched_instances(matching_instances, class_types)
        return [LogisticQueryResponse(**instance) for instance in matching_instances]

    def _get_query(self, config: LogisticQueryInput):
        return (
            """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?instance ?vehicle ?vehicleName ?vehicleAvailableQuantity ?vehicleTransportDistance ?service ?serviceName ?serviceTransportCO2e ?serviceExclusiveDownstreamCompanies ?serviceExclusiveUpstreamCompanies ?quote ?quoteMonetaryValuePerUnit ?quoteUnit ?quoteCurrency ?company
where {
    VALUES ?storageType { """ + f"{' '.join(map(lambda type: f"hydrogen_nrmm:{type}", config.storageTypes))}" + """ }
    GRAPH ?instance {
        ?vehicle hydrogen_nrmm:carries ?storageType ;
                rdfs:label ?vehicleName ;
                hydrogen_nrmm:availableQuantity ?vehicleAvailableQuantity ;
                hydrogen_nrmm:transportDistance ?vehicleTransportDistance ;.
        ?service rdf:type hydrogen_nrmm:LogisticService;
                rdfs:label ?serviceName ;
                hydrogen_nrmm:includes ?vehicle;.
        OPTIONAL { ?service hydrogen_nrmm:transportCO2e ?serviceTransportCO2e. }
        OPTIONAL { ?service hydrogen_nrmm:typicalPricing ?quote;.
                ?quote hydrogen_nrmm:monetaryValuePerUnit ?quoteMonetaryValuePerUnit;
                        hydrogen_nrmm:unit ?quoteUnit;
                        hydrogen_nrmm:currency ?quoteCurrency;. }
        OPTIONAL { ?service hydrogen_nrmm:exclusiveDownstreamCompanies ?serviceExclusiveDownstreamCompanies;. }
        OPTIONAL { ?service hydrogen_nrmm:exclusiveUpstreamCompanies ?serviceExclusiveUpstreamCompanies;. }
        ?company hydrogen_nrmm:provides ?service;.
    }
}
"""
        )
