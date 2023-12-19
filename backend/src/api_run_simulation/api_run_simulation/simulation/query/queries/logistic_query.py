from decimal import Decimal
from simulation.query.queries import (
    BaseQuery,
    LogisticQueryResponse,
    LogisticQueryInput,
)
from simulation.query.queries.hydrogen_nrmm_optional import (
    Storage,
    LogisticService,
    Vehicle,
)


class LogisticQuery(BaseQuery):
    def query(self, config: LogisticQueryInput) -> list[LogisticQueryResponse]:
        return super().query(config)

    def _parse_query(self, resp_obj) -> list[LogisticQueryResponse]:
        bindings = resp_obj["results"]["bindings"]
        class_types = {
            "storage": Storage,
            "service": LogisticService,
            "vehicle": Vehicle,
            "projectDistance": Decimal,
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
PREFIX omgeo: <http://www.ontotext.com/owlim/geo#>
select ?storage ?storageName ?storageAvailableQuantity ?storageCapacity ?vehicle ?vehicleName ?vehicleAvailableQuantity ?vehicleTransportDistance ?service ?serviceName ?projectDistance
where {
    ?storage rdf:type hydrogen_nrmm:TubeTrailer ;
             rdfs:label ?storageName ;
             hydrogen_nrmm:availableQuantity ?storageAvailableQuantity ;
             hydrogen_nrmm:capacity ?storageCapacity ;.
    ?vehicle hydrogen_nrmm:carries hydrogen_nrmm:TubeTrailer ;
             rdfs:label ?vehicleName ;
             hydrogen_nrmm:availableQuantity ?vehicleAvailableQuantity ;
             hydrogen_nrmm:basedAt ?vehicleBasedAt ;
             hydrogen_nrmm:transportDistance ?vehicleTransportDistance ;.
    ?service rdf:type hydrogen_nrmm:LogisticService;
             rdfs:label ?serviceName ;
             hydrogen_nrmm:includes ?storage;
             hydrogen_nrmm:includes ?vehicle
    FILTER(?storageCapacity >= """
            + f"{config.minStorage}"
            + """)
    
    ?vehicleBasedAt hydrogen_nrmm:lat ?lat ;
                    hydrogen_nrmm:long ?long ;.
    BIND(omgeo:distance(?lat, ?long, """
            + f"{config.lat}, {config.long}"
            + """) * 0.621371 as ?projectDistance)
}
"""
        )
