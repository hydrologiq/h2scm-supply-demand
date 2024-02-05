from dataclasses import dataclass
from typing import Optional
import simulation.business.outputs as BusinessOutputs

from simulation.query.queries import LogisticQueryResponse
from tests.helpers import to_id


@dataclass
class LogisticResponse:
    vehicle: str
    vehicleName: str
    vehicleAvailableQuantity: float
    vehicleTransportDistance: float
    service: str
    serviceName: str
    quote: str
    quoteMonetaryValue: float
    serviceTransportCO2e: Optional[float] = None

    def query_response(self) -> LogisticQueryResponse:
        service = {"id": to_id(self.service), "name": self.serviceName}
        if self.serviceTransportCO2e is not None:
            service["transportCO2e"] = self.serviceTransportCO2e

        return LogisticQueryResponse(
            vehicle={
                "id": to_id(self.vehicle),
                "name": self.vehicleName,
                "availableQuantity": self.vehicleAvailableQuantity,
                "transportDistance": self.vehicleTransportDistance,
            },
            service=service,
            quote={"id": to_id(self.quote), "monetaryValue": self.quoteMonetaryValue},
        )

    def response_binding(self) -> object:
        binding = {
            "vehicle": {
                "type": "uri",
                "value": f"https://w3id.org/hydrologiq/hydrogen/nrmm{self.vehicle}",
            },
            "vehicleName": {"type": "literal", "value": f"{self.vehicleName}"},
            "vehicleAvailableQuantity": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": f"{self.vehicleAvailableQuantity}",
            },
            "vehicleTransportDistance": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": f"{self.vehicleTransportDistance}",
            },
            "service": {
                "type": "uri",
                "value": f"https://w3id.org/hydrologiq/hydrogen/nrmm{self.service}",
            },
            "serviceName": {"type": "literal", "value": f"{self.serviceName}"},
            "quote": {
                "type": "uri",
                "value": f"https://w3id.org/hydrologiq/hydrogen/nrmm{self.quote}",
            },
            "quoteMonetaryValue": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": f"{self.quoteMonetaryValue}",
            },
        }

        if self.serviceTransportCO2e is not None:
            binding["serviceTransportCO2e"] = {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": f"{self.serviceTransportCO2e}",
            }

        return binding


def logistic_query_response_json(responses: list[LogisticResponse]):
    return {
        "head": {
            "vars": [
                "vehicle",
                "vehicleName",
                "vehicleAvailableQuantity",
                "vehicleTransportDistance",
                "service",
                "serviceName",
                "serviceTransportCO2e",
                "quote",
                "quoteMonetaryValue",
            ]
        },
        "results": {
            "bindings": [response.response_binding() for response in responses]
        },
    }


def sparql_query_logistic(
    storage_type: BusinessOutputs.Storage = BusinessOutputs.Storage.TubeTrailer,
):
    return (
        """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?vehicle ?vehicleName ?vehicleAvailableQuantity ?vehicleTransportDistance ?service ?serviceName ?serviceTransportCO2e ?quote ?quoteMonetaryValue
where {
    ?vehicle hydrogen_nrmm:carries hydrogen_nrmm:"""
        + f"{storage_type}"
        + """ ;
             rdfs:label ?vehicleName ;
             hydrogen_nrmm:availableQuantity ?vehicleAvailableQuantity ;
             hydrogen_nrmm:transportDistance ?vehicleTransportDistance ;.
    ?service rdf:type hydrogen_nrmm:LogisticService;
             rdfs:label ?serviceName ;
             hydrogen_nrmm:includes ?vehicle;.
    OPTIONAL { ?service hydrogen_nrmm:transportCO2e ?serviceTransportCO2e. }
    OPTIONAL { ?service hydrogen_nrmm:typicalPricing ?quote;.
               ?quote hydrogen_nrmm:monetaryValuePerUnit ?quoteMonetaryValue. }
}
"""
    )
