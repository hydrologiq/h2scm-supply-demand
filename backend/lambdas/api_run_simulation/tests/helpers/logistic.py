from dataclasses import dataclass

from api_run_simulation.simulation.query.queries import LogisticQueryResponse
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
            ]
        },
        "results": {
            "bindings": [response.response_binding() for response in responses]
        },
    }


def logistic_query_sparql(minStorage: int, lat: float, long: float):
    return (
        """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX omgeo: <http://www.ontotext.com/owlim/geo#>
select ?storage ?storageName ?storageAvailableQuantity ?storageCapacity ?vehicle ?vehicleName ?vehicleAvailableQuantity ?vehicleTransportDistance ?service ?serviceName ?projectDistance ?distro ?distroName ?distroLat ?distroLong
where {
    ?storage rdf:type hydrogen_nrmm:TubeTrailer ;
             rdfs:label ?storageName ;
             hydrogen_nrmm:availableQuantity ?storageAvailableQuantity ;
             hydrogen_nrmm:capacity ?storageCapacity ;.
    ?vehicle hydrogen_nrmm:carries hydrogen_nrmm:TubeTrailer ;
             rdfs:label ?vehicleName ;
             hydrogen_nrmm:availableQuantity ?vehicleAvailableQuantity ;
             hydrogen_nrmm:basedAt ?distro ;
             hydrogen_nrmm:transportDistance ?vehicleTransportDistance ;.
    ?service rdf:type hydrogen_nrmm:LogisticService;
             rdfs:label ?serviceName ;
             hydrogen_nrmm:includes ?storage;
             hydrogen_nrmm:includes ?vehicle
    FILTER(?storageCapacity >= """
        + f"{minStorage}"
        + """)
    
    ?distro rdfs:label ?distroName ;
            hydrogen_nrmm:lat ?distroLat ;
            hydrogen_nrmm:long ?distroLong ;.
    BIND(omgeo:distance(?distroLat, ?distroLong, """
        + f"{lat}, {long}"
        + """) * 0.621371 as ?projectDistance)
}
"""
    )
