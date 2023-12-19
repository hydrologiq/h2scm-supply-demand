from decimal import Decimal
from simulation.query.queries import BaseQuery, LogisticQueryResponse
from simulation.query.queries.base_response import BaseQueryResponse
from simulation.query.queries.hydrogen_nrmm_optional import (
    Storage,
    LogisticService,
    Vehicle,
    YAMLRoot,
)


class LogisticQuery(BaseQuery):
    def query(self) -> list[LogisticQueryResponse]:
        return super().query()

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
        for i in range(len(matching_instances)):
            for instance in matching_instances[i]:
                if instance in class_types:
                    class_type = class_types[instance]

                    if issubclass(class_type, Decimal):
                        matching_instances[i][instance] = Decimal(
                            matching_instances[i][instance]
                        )
                    else:
                        matching_instances[i][instance] = class_type(
                            **matching_instances[i][instance]
                        )
        return [
            LogisticQueryResponse(
                instance["storage"],
                instance["service"],
                instance["vehicle"],
                instance["projectDistance"],
            )
            for instance in matching_instances
        ]

    def _get_query(self):
        return """
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
    FILTER(?storageCapacity >= 185)
    
    ?vehicleBasedAt hydrogen_nrmm:lat ?lat ;
                    hydrogen_nrmm:long ?long ;.
    BIND(omgeo:distance(?lat, ?long, 12.234, 43.221) * 0.621371 as ?projectDistance)
}
"""
