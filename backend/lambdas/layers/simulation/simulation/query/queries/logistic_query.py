from decimal import Decimal
from simulation.query.queries import (
    BaseQuery,
    LogisticQueryResponse,
    LogisticQueryInput,
)
from simulation.query.queries.hydrogen_nrmm_optional import (
    Price,
    Storage,
    LogisticService,
    Vehicle,
)


class LogisticQuery(BaseQuery):
    def query(self, config: LogisticQueryInput) -> list[LogisticQueryResponse]:
        return super().query(config)

    def _parse_query(self, resp_obj) -> list[LogisticQueryResponse]:
        if "results" not in resp_obj:
            raise Exception(f"Could not query with error -- {resp_obj}")
        bindings = resp_obj["results"]["bindings"]
        class_types = {
            "storage": Storage,
            "service": LogisticService,
            "vehicle": Vehicle,
            "price": Price,
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
select ?storage ?storageName ?storageAvailableQuantity ?storageCapacity ?vehicle ?vehicleName ?vehicleAvailableQuantity ?vehicleTransportDistance ?service ?serviceName ?serviceTransportCO2e ?price ?priceMonetaryValue
where {
    ?storage rdf:type hydrogen_nrmm:"""
            + f"{config.storageType}"
            + """ ;
             rdfs:label ?storageName ;
             hydrogen_nrmm:availableQuantity ?storageAvailableQuantity ;
             hydrogen_nrmm:capacity ?storageCapacity ;.
    FILTER(?storageCapacity >= """
            + f"{config.minStorage}"
            + """)
    ?vehicle hydrogen_nrmm:carries hydrogen_nrmm:"""
            + f"{config.storageType}"
            + """ ;
             rdfs:label ?vehicleName ;
             hydrogen_nrmm:availableQuantity ?vehicleAvailableQuantity ;
             hydrogen_nrmm:transportDistance ?vehicleTransportDistance ;.
    ?service rdf:type hydrogen_nrmm:LogisticService;
             rdfs:label ?serviceName ;
             hydrogen_nrmm:includes ?storage;
             hydrogen_nrmm:includes ?vehicle;
             hydrogen_nrmm:typicalPricing ?quote;.
    OPTIONAL { ?service hydrogen_nrmm:transportCO2e ?serviceTransportCO2e. }
    ?quote hydrogen_nrmm:price ?price;.
    ?price hydrogen_nrmm:monetaryValue ?priceMonetaryValue;
             hydrogen_nrmm:unit ?priceUnit;.
}
"""
        )
