from decimal import Decimal
from simulation.query.queries import (
    BaseQuery,
    StorageQueryResponse,
    StorageQueryInput,
)
from simulation.query.queries.hydrogen_nrmm_optional import (
    Quote,
    Storage,
    Rental,
    Company,
)


class StorageQuery(BaseQuery):
    def query(self, config: StorageQueryInput) -> list[StorageQueryResponse]:
        return super().query(config)

    def _parse_query(self, resp_obj) -> list[StorageQueryResponse]:
        if "results" not in resp_obj:
            raise Exception(f"Could not query with error -- {resp_obj}")
        bindings = resp_obj["results"]["bindings"]
        class_types = {
            "storage": Storage,
            "service": Rental,
            "quote": Quote,
            "company": Company,
        }
        matching_instances = self._get_matching_instances(
            bindings,
            class_types.keys(),
        )
        self._convert_matched_instances(matching_instances, class_types)
        return [StorageQueryResponse(**instance) for instance in matching_instances]

    def _get_query(self, config: StorageQueryInput):
        return (
            """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?storage ?storageName ?storageAvailableQuantity ?storageCapacity ?service ?serviceName ?serviceExclusiveDownstreamCompanies ?serviceExclusiveUpstreamCompanies ?quote ?quoteMonetaryValue ?company
where {
    ?storage rdf:type hydrogen_nrmm:Storage ;
             rdfs:label ?storageName ;
             hydrogen_nrmm:availableQuantity ?storageAvailableQuantity ;
             hydrogen_nrmm:capacity ?storageCapacity ;.
    FILTER(?storageCapacity * ?storageAvailableQuantity >= """
            + f"{config.totalFuel}"
            + """)
    ?service rdf:type hydrogen_nrmm:Rental;
             rdfs:label ?serviceName ;
             hydrogen_nrmm:includes ?storage;
    OPTIONAL { ?service hydrogen_nrmm:typicalPricing ?quote;.
               ?quote hydrogen_nrmm:monetaryValuePerUnit ?quoteMonetaryValue. }
    OPTIONAL { ?service hydrogen_nrmm:exclusiveDownstreamCompanies ?serviceExclusiveDownstreamCompanies;. }
    OPTIONAL { ?service hydrogen_nrmm:exclusiveUpstreamCompanies ?serviceExclusiveUpstreamCompanies;. }
    ?company hydrogen_nrmm:provides ?service;.
}
"""
        )
