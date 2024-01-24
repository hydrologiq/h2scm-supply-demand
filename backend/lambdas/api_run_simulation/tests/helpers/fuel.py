from dataclasses import dataclass
from api_run_simulation.simulation.query.queries import FuelQueryResponse
from tests.helpers import to_id


@dataclass
class FuelResponse:
    producer: str
    producerName: str
    producerDailyOfftakeCapacity: float
    dispenser: str
    dispenserName: str
    dispenserLat: float
    dispenserLong: float
    dispenserFillingStationCapacity: int
    dispenserFillRate: float
    service: str
    serviceName: str

    def query_response(self) -> FuelQueryResponse:
        return FuelQueryResponse(
            producer={
                "id": to_id(self.producer),
                "name": self.producerName,
                "dailyOfftakeCapacity": self.producerDailyOfftakeCapacity,
            },
            service={"id": to_id(self.service), "name": self.serviceName},
            dispenser={
                "id": to_id(self.dispenser),
                "name": self.dispenserName,
                "lat": self.dispenserLat,
                "long": self.dispenserLong,
                "fillRate": self.dispenserFillRate,
                "fillingStationCapacity": self.dispenserFillingStationCapacity,
            },
        )

    def response_binding(self) -> object:
        return {
            "producer": {
                "type": "uri",
                "value": f"https://w3id.org/hydrologiq/hydrogen/nrmm{self.producer}",
            },
            "producerName": {"type": "literal", "value": f"{self.producerName}"},
            "producerDailyOfftakeCapacity": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": f"{self.producerDailyOfftakeCapacity}",
            },
            "dispenser": {
                "type": "uri",
                "value": f"https://w3id.org/hydrologiq/hydrogen/nrmm{self.dispenser}",
            },
            "dispenserName": {"type": "literal", "value": f"{self.dispenserName}"},
            "dispenserLat": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": f"{self.dispenserLat}",
            },
            "dispenserLong": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": f"{self.dispenserLong}",
            },
            "dispenserFillingStationCapacity": {
                "datatype": "http://www.w3.org/2001/XMLSchema#integer",
                "type": "literal",
                "value": f"{self.dispenserFillingStationCapacity}",
            },
            "dispenserFillRate": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": f"{self.dispenserFillRate}",
            },
            "service": {
                "type": "uri",
                "value": f"https://w3id.org/hydrologiq/hydrogen/nrmm{self.service}",
            },
            "serviceName": {"type": "literal", "value": f"{self.serviceName}"},
        }


def fuel_query_response_json(responses: list[FuelResponse]):
    return {
        "head": {
            "vars": [
                "producer",
                "producerName",
                "producerDailyOfftakeCapacity",
                "dispenser",
                "dispenserName",
                "dispenserLat",
                "dispenserLong",
                "dispenserFillingStationCapacity",
                "dispenserFillRate",
                "service",
                "serviceName",
            ]
        },
        "results": {
            "bindings": [response.response_binding() for response in responses]
        },
    }


def fuel_query_sparql(sum_of_fuel: float):
    return (
        """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?producer ?producerName ?producerDailyOfftakeCapacity ?dispenser ?dispenserName ?dispenserLat ?dispenserLong ?dispenserFillingStationCapacity ?dispenserFillRate ?service ?serviceName
        where { 
            ?producer rdfs:label ?producerName ;
                      hydrogen_nrmm:dailyOfftakeCapacity ?producerDailyOfftakeCapacity ;
                      hydrogen_nrmm:basedAt ?dispenser ;.
            FILTER(?producerDailyOfftakeCapacity >= """
        + f"{sum_of_fuel}"
        + """)
            ?dispenser rdfs:label ?dispenserName;
                      hydrogen_nrmm:lat ?dispenserLat;
                      hydrogen_nrmm:long ?dispenserLong;
                      hydrogen_nrmm:fillingStationCapacity ?dispenserFillingStationCapacity;
                      hydrogen_nrmm:fillRate ?dispenserFillRate;.
            ?service hydrogen_nrmm:includes ?producer ;
                      rdfs:label ?serviceName;
        }
    """
    )
