from dataclasses import dataclass
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

    def query_response(self) -> StorageQueryResponse:
        service = {"id": to_id(self.service), "name": self.serviceName}
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
    minStorage: int,
    storage_type: BusinessOutputs.Storage = BusinessOutputs.Storage.TubeTrailer,
):
    return (
        """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?storage ?storageName ?storageAvailableQuantity ?storageCapacity ?service ?serviceName ?quote ?quoteMonetaryValue
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
               ?quote hydrogen_nrmm:monetaryValue ?quoteMonetaryValue. }
}
"""
    )
