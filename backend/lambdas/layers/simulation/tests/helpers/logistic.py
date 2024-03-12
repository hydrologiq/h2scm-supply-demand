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
    quoteMonetaryValuePerUnit: float
    quoteUnit: str
    quoteCurrency: str
    company: str
    serviceTransportCO2e: Optional[float] = None
    serviceExclusiveDownstreamCompanies: Optional[str] = None
    serviceExclusiveUpstreamCompanies: Optional[str] = None
    instance: Optional[str] = ""

    def query_response(self) -> LogisticQueryResponse:
        service = {"id": to_id(self.service), "name": self.serviceName}
        if self.serviceTransportCO2e is not None:
            service["transportCO2e"] = self.serviceTransportCO2e
        if self.serviceExclusiveDownstreamCompanies is not None:
            service["exclusiveDownstreamCompanies"] = (
                to_id(self.serviceExclusiveDownstreamCompanies)
            )
        if self.serviceExclusiveUpstreamCompanies is not None:
            service["exclusiveUpstreamCompanies"] = (
                to_id(self.serviceExclusiveUpstreamCompanies)
            )
        return LogisticQueryResponse(
            vehicle={
                "id": to_id(self.vehicle),
                "name": self.vehicleName,
                "availableQuantity": self.vehicleAvailableQuantity,
                "transportDistance": self.vehicleTransportDistance,
            },
            service=service,
            quote={
                "id": to_id(self.quote),
                "monetaryValuePerUnit": self.quoteMonetaryValuePerUnit,
                "currency": self.quoteCurrency,
                "unit": self.quoteUnit
            },
            company={"id": to_id(self.company)},
            instance=to_id(self.instance)
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
            "quoteMonetaryValuePerUnit": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": f"{self.quoteMonetaryValuePerUnit}",
            },
            "quoteUnit": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": f"{self.quoteUnit}",
            },
            "quoteCurrency": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": f"{self.quoteCurrency}",
            },
            "company": {
                "type": "uri",
                "value": f"https://w3id.org/hydrologiq/hydrogen/nrmm{self.company}",
            },
            "instance": {
                "type": "uri",
                "value": f"https://w3id.org/hydrologiq/hydrogen/nrmm{self.instance}",
            },
        }
        if self.serviceTransportCO2e is not None:
            binding["serviceTransportCO2e"] = {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": f"{self.serviceTransportCO2e}",
            }
        if self.serviceExclusiveDownstreamCompanies is not None:
            binding["serviceExclusiveDownstreamCompanies"] = {
                "type": "uri",
                "value": f"https://w3id.org/hydrologiq/hydrogen/nrmm{self.serviceExclusiveDownstreamCompanies}",
            }
        if self.serviceExclusiveUpstreamCompanies is not None:
            binding["serviceExclusiveUpstreamCompanies"] = {
                "type": "uri",
                "value": f"https://w3id.org/hydrologiq/hydrogen/nrmm{self.serviceExclusiveUpstreamCompanies}",
            }
        return binding


def logistic_query_response_json(responses: list[LogisticResponse]):
    return {
        "head": {"vars": []},
        "results": {
            "bindings": [response.response_binding() for response in responses]
        },
    }


def sparql_query_logistic(
    storage_types: list[BusinessOutputs.Storage] = [BusinessOutputs.Storage.TubeTrailer],
):
    return (
        """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?instance ?vehicle ?vehicleName ?vehicleAvailableQuantity ?vehicleTransportDistance ?service ?serviceName ?serviceTransportCO2e ?serviceExclusiveDownstreamCompanies ?serviceExclusiveUpstreamCompanies ?quote ?quoteMonetaryValuePerUnit ?quoteUnit ?quoteCurrency ?company
where {
    VALUES ?storageType { """ + f"{' '.join(map(lambda type: f"hydrogen_nrmm:{type}", storage_types))}" + """ }
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
