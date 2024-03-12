from dataclasses import dataclass
from typing import Optional
import simulation.business.outputs as BusinessOutputs

from simulation.query.queries import StorageQueryResponse
from simulation.query.queries.hydrogen_nrmm_optional import (
    ManifoldCylinderPallet,
    TubeTrailer,
)
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
    quoteMonetaryValuePerUnit: float
    quoteUnit: str
    quoteCurrency: str
    company: str
    storageType: BusinessOutputs.Storage = BusinessOutputs.Storage.TubeTrailer
    serviceExclusiveDownstreamCompanies: Optional[str] = None
    serviceExclusiveUpstreamCompanies: Optional[str] = None
    instance: Optional[str] = ""

    def query_response(self) -> StorageQueryResponse:
        service = {"id": to_id(self.service), "name": self.serviceName}
        if self.serviceExclusiveDownstreamCompanies is not None:
            service["exclusiveDownstreamCompanies"] = to_id(
                self.serviceExclusiveDownstreamCompanies
            )
        if self.serviceExclusiveUpstreamCompanies is not None:
            service["exclusiveUpstreamCompanies"] = to_id(
                self.serviceExclusiveUpstreamCompanies
            )
        storage = {
            "id": to_id(self.storage),
            "name": self.storageName,
            "availableQuantity": self.storageAvailableQuantity,
            "capacity": self.storageCapacity,
        }
        return StorageQueryResponse(
            storage=(
                ManifoldCylinderPallet(**storage)
                if (self.storageType == BusinessOutputs.Storage.ManifoldCylinderPallet)
                else TubeTrailer(**storage)
            ),
            service=service,
            quote={
                "id": to_id(self.quote),
                "monetaryValuePerUnit": self.quoteMonetaryValuePerUnit,
                "currency": self.quoteCurrency,
                "unit": self.quoteUnit,
            },
            company={"id": to_id(self.company)},
            instance=to_id(self.instance),
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
            "storageType": {
                "type": "uri",
                "value": f"https://w3id.org/hydrologiq/hydrogen/nrmm{self.storageType}",
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
        "head": {"vars": []},
        "results": {
            "bindings": [response.response_binding() for response in responses]
        },
    }


def sparql_query_storage(totalFuel: int):
    return (
        """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?instance ?storage ?storageName ?storageAvailableQuantity ?storageCapacity ?storageType ?service ?serviceName ?serviceExclusiveDownstreamCompanies ?serviceExclusiveUpstreamCompanies ?quote ?quoteMonetaryValuePerUnit ?quoteUnit ?quoteCurrency ?company
where {
    VALUES ?storageType { hydrogen_nrmm:TubeTrailer hydrogen_nrmm:ManifoldCylinderPallet }
    GRAPH ?instance {
        ?storage rdf:type ?storageType;
                rdfs:label ?storageName ;
                hydrogen_nrmm:availableQuantity ?storageAvailableQuantity ;
                hydrogen_nrmm:capacity ?storageCapacity ;.
        FILTER(?storageCapacity * ?storageAvailableQuantity >= """
        + f"{int(totalFuel)}"
        + """)
        ?service rdf:type hydrogen_nrmm:Rental;
                rdfs:label ?serviceName ;
                hydrogen_nrmm:includes ?storage;
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
