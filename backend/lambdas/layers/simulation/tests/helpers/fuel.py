from dataclasses import dataclass
from typing import Optional
from simulation.query.queries import FuelQueryResponse
from simulation.query.queries.hydrogen_nrmm_optional import ElectrolyticHydrogen, SteamMethaneReformingHydrogen
from tests.helpers import to_id
import simulation.business.outputs as BusinessOutputs


@dataclass
class FuelResponse():
    producer: str
    producerName: str
    producerWeeklyProductionCapacity: float
    producerType: BusinessOutputs.Producer
    dispenser: str
    dispenserName: str
    dispenserLat: float
    dispenserLong: float
    service: str
    serviceName: str
    quote: str
    quoteMonetaryValuePerUnit: float
    quoteUnit: str
    quoteCurrency: str
    company: str
    producerProductionCO2e: Optional[float] = None
    serviceExclusiveDownstreamCompanies: Optional[str] = None
    serviceExclusiveUpstreamCompanies: Optional[str] = None
    producerSource: Optional[str] = None
    producerStoredIn: Optional[list[BusinessOutputs.Storage]] = None
    instance: Optional[str] = ""
    
    def __post_init__(self):
        if self.producerStoredIn is None:
            self.producerStoredIn = [BusinessOutputs.Storage.TubeTrailer]
    
    def query_response(self) -> FuelQueryResponse:
        producer = {
            "id": to_id(self.producer),
            "name": self.producerName,
            "weeklyProductionCapacity": self.producerWeeklyProductionCapacity,
        }

        if isinstance(self.producerStoredIn, list):
            producer["storedIn"] = [to_id(storedIn) for storedIn in self.producerStoredIn]

        if self.producerProductionCO2e is not None:
            producer["productionCO2e"] = self.producerProductionCO2e

        if self.producerSource is not None:
            producer["source"] = self.producerSource

        service = {"id": to_id(self.service), "name": self.serviceName}
        if self.serviceExclusiveDownstreamCompanies is not None:
            service["exclusiveDownstreamCompanies"] = (
                to_id(self.serviceExclusiveDownstreamCompanies)
            )
        if self.serviceExclusiveUpstreamCompanies is not None:
            service["exclusiveUpstreamCompanies"] = (
                to_id(self.serviceExclusiveUpstreamCompanies)
            )
        return FuelQueryResponse(
            producer=(
                ElectrolyticHydrogen(**producer)
                if (self.producerType == BusinessOutputs.Producer.ElectrolyticHydrogen)
                else SteamMethaneReformingHydrogen(**producer)
            ),
            service=service,
            dispenser={
                "id": to_id(self.dispenser),
                "name": self.dispenserName,
                "lat": self.dispenserLat,
                "long": self.dispenserLong,
            },
            quote={
                "id": to_id(self.quote),
                "monetaryValuePerUnit": self.quoteMonetaryValuePerUnit,
                "currency": self.quoteCurrency,
                "unit": self.quoteUnit
            },
            company={"id": to_id(self.company)},
            instance=to_id(self.instance)
        )

    def response_bindings(self) -> list[object]:
        if isinstance(self.producerStoredIn, list):
            return [self.response_binding(storedIn) for storedIn in self.producerStoredIn]
        else:
            return [self.response_binding()]

    def response_binding(self, storedIn: Optional[BusinessOutputs.Storage] = None) -> object:
        binding = {
            "producer": {
                "type": "uri",
                "value": f"https://w3id.org/hydrologiq/hydrogen/nrmm{self.producer}",
            },
            "producerType": {"type": "literal", "value": f"{self.producerType}"},
            "producerName": {"type": "literal", "value": f"{self.producerName}"},
            "producerWeeklyProductionCapacity": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": f"{self.producerWeeklyProductionCapacity}",
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
        storedIn = [storedIn] if isinstance(storedIn, BusinessOutputs.Storage) else self.producerStoredIn
        if storedIn is not None:
            binding["producerStoredIn"] = {"type": "literal", "value": f"{to_id(storedIn[0])}"}
        
        if self.producerSource is not None:
            binding["producerSource"] = {
                "type": "literal",
                "value": f"{self.producerSource}",
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


def flatten_comprehension(matrix):
    return [item for row in matrix for item in row]

def fuel_query_response_json(responses: list[FuelResponse]):
    return {
        "head": {"vars": []},
        "results": {
            "bindings": flatten_comprehension([response.response_bindings() for response in responses])
        },
    }


def sparql_query_fuel(
    sum_of_fuel: int,
    storage_types: BusinessOutputs.Storage = [BusinessOutputs.Storage.TubeTrailer],
):
    return (
        """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?instance ?producer ?producerStoredIn ?producerType ?producerName ?producerSource ?producerWeeklyProductionCapacity ?producerProductionCO2e ?dispenser ?dispenserName ?dispenserLat ?dispenserLong ?service ?serviceName ?serviceExclusiveDownstreamCompanies ?serviceExclusiveUpstreamCompanies ?quote ?quoteMonetaryValuePerUnit ?quoteUnit ?quoteCurrency ?company
where {
    VALUES ?producerType { hydrogen_nrmm:ElectrolyticHydrogen hydrogen_nrmm:SteamMethaneReformingHydrogen }
    GRAPH ?instance {
        ?producer   rdf:type ?producerType ;
                    rdfs:label ?producerName ;
                    hydrogen_nrmm:weeklyProductionCapacity ?producerWeeklyProductionCapacity ;
                    hydrogen_nrmm:storedIn ?producerStoredIn ;
                    hydrogen_nrmm:basedAt ?dispenser ;.
        FILTER(?producerWeeklyProductionCapacity >= """
            + f"{int(sum_of_fuel)}"
            + """ && ?producerStoredIn IN ("""
            + f"{', '.join(map(lambda type: f"hydrogen_nrmm:{type}", storage_types))}"
            + """))
        OPTIONAL { ?producer hydrogen_nrmm:productionCO2e ?producerProductionCO2e }
        OPTIONAL { ?producer hydrogen_nrmm:source ?producerSource }
        ?dispenser rdfs:label ?dispenserName;
                    hydrogen_nrmm:lat ?dispenserLat;
                    hydrogen_nrmm:long ?dispenserLong;.
        ?service hydrogen_nrmm:includes ?producer ;
                    rdfs:label ?serviceName;
        OPTIONAL { ?service hydrogen_nrmm:typicalPricing ?quote;.
                    ?quote hydrogen_nrmm:monetaryValuePerUnit ?quoteMonetaryValuePerUnit;
                            hydrogen_nrmm:unit ?quoteUnit;
                            hydrogen_nrmm:currency ?quoteCurrency;. }
        OPTIONAL { ?service hydrogen_nrmm:exclusiveDownstreamCompanies ?serviceExclusiveDownstreamCompanies;. }
        OPTIONAL { ?service hydrogen_nrmm:exclusiveUpstreamCompanies ?serviceExclusiveUpstreamCompanies;. }
        ?company hydrogen_nrmm:provides ?service;.
    }
}"""
    )
