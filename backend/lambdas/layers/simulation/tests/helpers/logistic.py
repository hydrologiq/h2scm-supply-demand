from dataclasses import dataclass
from typing import Optional
import simulation.business.outputs as BusinessOutputs

from simulation.query.queries import LogisticQueryResponse
from tests.helpers import to_id


@dataclass
class LogisticResponse:
    storage: str
    storageName: str
    storageAvailableQuantity: float
    storageCapacity: float
    vehicle: str
    vehicleName: str
    vehicleAvailableQuantity: float
    vehicleTransportDistance: float
    service: str
    serviceName: str
    price: str
    priceMonetaryValue: float
    serviceTransportCO2e: Optional[float] = None

    def query_response(self) -> LogisticQueryResponse:
        service = {"id": to_id(self.service), "name": self.serviceName}
        if self.serviceTransportCO2e is not None:
            service["transportCO2e"] = self.serviceTransportCO2e

        return LogisticQueryResponse(
            storage={
                "id": to_id(self.storage),
                "name": self.storageName,
                "availableQuantity": self.storageAvailableQuantity,
                "capacity": self.storageCapacity,
            },
            vehicle={
                "id": to_id(self.vehicle),
                "name": self.vehicleName,
                "availableQuantity": self.vehicleAvailableQuantity,
                "transportDistance": self.vehicleTransportDistance,
            },
            service=service,
            price={"id": to_id(self.price), "monetaryValue": self.priceMonetaryValue},
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
            "price": {
                "type": "uri",
                "value": f"https://w3id.org/hydrologiq/hydrogen/nrmm{self.price}",
            },
            "priceMonetaryValue": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": f"{self.priceMonetaryValue}",
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
                "storage",
                "storageName",
                "storageAvailableQuantity",
                "storageCapacity",
                "vehicle",
                "vehicleName",
                "vehicleAvailableQuantity",
                "vehicleTransportDistance",
                "service",
                "serviceName",
                "serviceTransportCO2e",
                "price",
                "priceMonetaryValue",
            ]
        },
        "results": {
            "bindings": [response.response_binding() for response in responses]
        },
    }


def sparql_query_logistic(
    minStorage: int,
    storage_type: BusinessOutputs.Storage = BusinessOutputs.Storage.TubeTrailer,
):
    return (
        """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?storage ?storageName ?storageAvailableQuantity ?storageCapacity ?vehicle ?vehicleName ?vehicleAvailableQuantity ?vehicleTransportDistance ?service ?serviceName ?serviceTransportCO2e ?price ?priceMonetaryValue
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
    ?vehicle hydrogen_nrmm:carries hydrogen_nrmm:"""
        + f"{storage_type}"
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
