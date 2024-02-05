from dataclasses import dataclass
from typing import Optional
import simulation.business.outputs as BusinessOutputs

from simulation.query.queries import StorageQueryResponse
from tests.helpers import to_id


@dataclass
class StorageResponse:
    storage: str
    storageName: str
    storageAvailableQuantity: float
    storageCapacity: float
    service: str
    serviceName: str
    quote: str
    quoteMonetaryValue: float
    serviceExclusiveDownstreamCompanies: Optional[str] = None
    serviceExclusiveUpstreamCompanies: Optional[str] = None

    def query_response(self) -> StorageQueryResponse:
        service = {"id": to_id(self.service), "name": self.serviceName}
        if self.serviceExclusiveDownstreamCompanies is not None:
            service["exclusiveDownstreamCompanies"] = (
                self.serviceExclusiveDownstreamCompanies
            )
        if self.serviceExclusiveUpstreamCompanies is not None:
            service["exclusiveUpstreamCompanies"] = (
                self.serviceExclusiveUpstreamCompanies
            )
        return StorageQueryResponse(
            storage={
                "id": to_id(self.storage),
                "name": self.storageName,
                "availableQuantity": self.storageAvailableQuantity,
                "capacity": self.storageCapacity,
            },
            service=service,
            quote={"id": to_id(self.quote), "monetaryValue": self.quoteMonetaryValue},
        )

    def response_binding(self) -> object:
        binding = {
            "storage": {
                "type": "uri",
                "value": f"https://w3id.org/hydrologiq/hydrogen/nrmm{self.storage}",
            },
            "storageName": {"type": "literal", "value": f"{self.storageName}"},
            "storageAvailableQuantity": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": f"{self.storageAvailableQuantity}",
            },
            "storageCapacity": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": f"{self.storageCapacity}",
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


def storage_query_response_json(responses: list[StorageResponse]):
    return {
        "head": {
            "vars": [
                "storage",
                "storageName",
                "storageAvailableQuantity",
                "storageCapacity",
                "service",
                "serviceName",
                "quote",
                "quoteMonetaryValue",
            ]
        },
        "results": {
            "bindings": [response.response_binding() for response in responses]
        },
    }


def sparql_query_storage(
    minStorage: float,
    storage_type: BusinessOutputs.Storage = BusinessOutputs.Storage.TubeTrailer,
):
    return (
        """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?storage ?storageName ?storageAvailableQuantity ?storageCapacity ?service ?serviceName ?serviceExclusiveDownstreamCompanies ?serviceExclusiveUpstreamCompanies ?quote ?quoteMonetaryValue
where {
    ?storage rdf:type hydrogen_nrmm:"""
        + f"{storage_type}"
        + """ ;
             rdfs:label ?storageName ;
             hydrogen_nrmm:availableQuantity ?storageAvailableQuantity ;
             hydrogen_nrmm:capacity ?storageCapacity ;.
    FILTER(?storageCapacity >= """
        + f"{minStorage}"
        + """)
    ?service rdf:type hydrogen_nrmm:Rental;
             rdfs:label ?serviceName ;
             hydrogen_nrmm:includes ?storage;
    OPTIONAL { ?service hydrogen_nrmm:typicalPricing ?quote;.
               ?quote hydrogen_nrmm:monetaryValuePerUnit ?quoteMonetaryValue. }
    OPTIONAL { ?service hydrogen_nrmm:exclusiveDownstreamCompanies ?serviceExclusiveDownstreamCompanies;. }
    OPTIONAL { ?service hydrogen_nrmm:exclusiveUpstreamCompanies ?serviceExclusiveUpstreamCompanies;. }
}
"""
    )
