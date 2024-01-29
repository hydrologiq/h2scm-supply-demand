from dataclasses import dataclass

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
    projectDistance: float
    distro: str
    distroName: str
    distroLat: float
    distroLong: float
    price: str
    priceMonetaryValue: float

    def query_response(self) -> LogisticQueryResponse:
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
            service={"id": to_id(self.service), "name": self.serviceName},
            distro={
                "id": to_id(self.distro),
                "name": self.distroName,
                "lat": self.distroLat,
                "long": self.distroLong,
            },
            price={"id": to_id(self.price), "monetaryValue": self.priceMonetaryValue},
            projectDistance=self.projectDistance,
        )

    def response_binding(self) -> object:
        return {
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
            "projectDistance": {
                "datatype": "http://www.w3.org/2001/XMLSchema#float",
                "type": "literal",
                "value": f"{self.projectDistance}",
            },
            "distro": {
                "type": "uri",
                "value": f"https://w3id.org/hydrologiq/hydrogen/nrmm{self.distro}",
            },
            "distroName": {"type": "literal", "value": f"{self.distroName}"},
            "distroLat": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": f"{self.distroLat}",
            },
            "distroLong": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": f"{self.distroLong}",
            },
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
                "projectDistance",
                "distro",
                "distroName",
                "distroLat",
                "distroLong",
                "price",
                "priceMonetaryValue",
            ]
        },
        "results": {
            "bindings": [response.response_binding() for response in responses]
        },
    }
