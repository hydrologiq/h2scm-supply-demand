from dataclasses import dataclass
from typing import Optional
from simulation.query.queries import FuelQueryResponse
from tests.helpers import to_id
import simulation.business.outputs as BusinessOutputs


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
    quote: str
    quoteMonetaryValuePerUnit: float
    company: str
    producerProductionCO2e: Optional[float] = None
    serviceExclusiveDownstreamCompanies: Optional[str] = None
    serviceExclusiveUpstreamCompanies: Optional[str] = None

    def query_response(self) -> FuelQueryResponse:
        producer = {
            "id": to_id(self.producer),
            "name": self.producerName,
            "dailyOfftakeCapacity": self.producerDailyOfftakeCapacity,
        }

        if self.producerProductionCO2e is not None:
            producer["productionCO2e"] = self.producerProductionCO2e

        service = {"id": to_id(self.service), "name": self.serviceName}
        if self.serviceExclusiveDownstreamCompanies is not None:
            service["exclusiveDownstreamCompanies"] = (
                self.serviceExclusiveDownstreamCompanies
            )
        if self.serviceExclusiveUpstreamCompanies is not None:
            service["exclusiveUpstreamCompanies"] = (
                self.serviceExclusiveUpstreamCompanies
            )
        return FuelQueryResponse(
            producer=producer,
            service=service,
            dispenser={
                "id": to_id(self.dispenser),
                "name": self.dispenserName,
                "lat": self.dispenserLat,
                "long": self.dispenserLong,
                "fillRate": self.dispenserFillRate,
                "fillingStationCapacity": self.dispenserFillingStationCapacity,
            },
            quote={
                "id": to_id(self.quote),
                "monetaryValuePerUnit": self.quoteMonetaryValuePerUnit,
            },
            company={"id": to_id(self.company)},
        )

    def response_binding(self) -> object:
        binding = {
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
            "quote": {
                "type": "uri",
                "value": f"https://w3id.org/hydrologiq/hydrogen/nrmm{self.quote}",
            },
            "quoteMonetaryValuePerUnit": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": f"{self.quoteMonetaryValuePerUnit}",
            },
            "company": {
                "type": "uri",
                "value": f"https://w3id.org/hydrologiq/hydrogen/nrmm{self.company}",
            },
        }
        if self.producerProductionCO2e is not None:
            binding["producerProductionCO2e"] = {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": f"{self.producerProductionCO2e}",
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


def fuel_query_response_json(responses: list[FuelResponse]):
    return {
        "head": {"vars": []},
        "results": {
            "bindings": [response.response_binding() for response in responses]
        },
    }


def sparql_query_fuel(
    sum_of_fuel: float,
    storage_type: BusinessOutputs.Storage = BusinessOutputs.Storage.TubeTrailer,
):
    return (
        """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?producer ?producerName ?producerDailyOfftakeCapacity ?producerProductionCO2e ?dispenser ?dispenserName ?dispenserLat ?dispenserLong ?dispenserFillingStationCapacity ?dispenserFillRate ?service ?serviceName ?serviceExclusiveDownstreamCompanies ?serviceExclusiveUpstreamCompanies ?quote ?quoteMonetaryValuePerUnit ?company
where { 
    ?producer rdfs:label ?producerName ;
                hydrogen_nrmm:dailyOfftakeCapacity ?producerDailyOfftakeCapacity ;
                hydrogen_nrmm:storedIn ?producerStoredIn ;
                hydrogen_nrmm:basedAt ?dispenser ;.
    FILTER(?producerDailyOfftakeCapacity >= """
        + f"{sum_of_fuel}"
        + """ && ?producerStoredIn IN ("""
        + f"hydrogen_nrmm:{storage_type}"
        + """))
    OPTIONAL { ?producer hydrogen_nrmm:productionCO2e ?producerProductionCO2e. }
    ?dispenser rdfs:label ?dispenserName;
                hydrogen_nrmm:lat ?dispenserLat;
                hydrogen_nrmm:long ?dispenserLong;
                hydrogen_nrmm:fillingStationCapacity ?dispenserFillingStationCapacity;
                hydrogen_nrmm:fillRate ?dispenserFillRate;.
    ?service hydrogen_nrmm:includes ?producer ;
                rdfs:label ?serviceName;
    OPTIONAL { ?service hydrogen_nrmm:typicalPricing ?quote;.
                ?quote hydrogen_nrmm:monetaryValuePerUnit ?quoteMonetaryValuePerUnit. }
    OPTIONAL { ?service hydrogen_nrmm:exclusiveDownstreamCompanies ?serviceExclusiveDownstreamCompanies;. }
    OPTIONAL { ?service hydrogen_nrmm:exclusiveUpstreamCompanies ?serviceExclusiveUpstreamCompanies;. }
    ?company hydrogen_nrmm:provides ?service;.
}"""
    )
