import json


def sparql_query_logistic(minStorage: int, lat: float, long: float):
    return (
        """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX omgeo: <http://www.ontotext.com/owlim/geo#>
select ?storage ?storageName ?storageAvailableQuantity ?storageCapacity ?vehicle ?vehicleName ?vehicleAvailableQuantity ?vehicleTransportDistance ?service ?serviceName ?projectDistance
where {
    ?storage rdf:type hydrogen_nrmm:TubeTrailer ;
             rdfs:label ?storageName ;
             hydrogen_nrmm:availableQuantity ?storageAvailableQuantity ;
             hydrogen_nrmm:capacity ?storageCapacity ;.
    ?vehicle hydrogen_nrmm:carries hydrogen_nrmm:TubeTrailer ;
             rdfs:label ?vehicleName ;
             hydrogen_nrmm:availableQuantity ?vehicleAvailableQuantity ;
             hydrogen_nrmm:basedAt ?vehicleBasedAt ;
             hydrogen_nrmm:transportDistance ?vehicleTransportDistance ;.
    ?service rdf:type hydrogen_nrmm:LogisticService;
             rdfs:label ?serviceName ;
             hydrogen_nrmm:includes ?storage;
             hydrogen_nrmm:includes ?vehicle
    FILTER(?storageCapacity >= """
        + f"{minStorage}"
        + """)
    
    ?vehicleBasedAt hydrogen_nrmm:lat ?lat ;
                    hydrogen_nrmm:long ?long ;.
    BIND(omgeo:distance(?lat, ?long, """
        + f"{lat}, {long}"
        + """) * 0.621371 as ?projectDistance)
}
"""
    )


SPARQL_QUERY_LOGISTIC_RESPONSE = json.loads(
    """
      {
        "head": {
          "vars": [
            "storage",
            "storageName",
            "storageAvailable",
            "storageCapacity",
            "vehicle",
            "vehicleName",
            "vehicleAvailable",
            "service",
            "serviceName",
            "vehicleDist",
            "vehicleRange"
          ]
        },
        "results": {
          "bindings": [
            {
              "storage": {
                "type": "uri",
                "value": "https://w3id.org/hydrologiq/hydrogen/nrmm12"
              },
              "storageName": {
                "type": "literal",
                "value": "Tube Trailer 1"
              },
              "storageAvailableQuantity": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": "3"
              },
              "storageCapacity": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": "300"
              },
              "vehicle": {
                "type": "uri",
                "value": "https://w3id.org/hydrologiq/hydrogen/nrmm123"
              },
              "vehicleName": {
                "type": "literal",
                "value": "Vehicle 1"
              },
              "vehicleAvailableQuantity": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": "1"
              },
              "vehicleTransportDistance": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": "123"
              },
              "service": {
                "type": "uri",
                "value": "https://w3id.org/hydrologiq/hydrogen/nrmm1"
              },
              "serviceName": {
                "type": "literal",
                "value": "Service 1"
              },
              "projectDistance": {
                "datatype": "http://www.w3.org/2001/XMLSchema#float",
                "type": "literal",
                "value": "12.345"
              }
            },
            {
              "storage": {
                "type": "uri",
                "value": "https://w3id.org/hydrologiq/hydrogen/nrmm21"
              },
              "storageName": {
                "type": "literal",
                "value": "Tube Trailer 2"
              },
              "storageAvailableQuantity": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": "1"
              },
              "storageCapacity": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": "225"
              },
              "vehicle": {
                "type": "uri",
                "value": "https://w3id.org/hydrologiq/hydrogen/nrmm212"
              },
              "vehicleName": {
                "type": "literal",
                "value": "Vehicle 2"
              },
              "vehicleAvailableQuantity": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": "2"
              },
              "vehicleTransportDistance": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": "123"
              },
              "service": {
                "type": "uri",
                "value": "https://w3id.org/hydrologiq/hydrogen/nrmm2"
              },
              "serviceName": {
                "type": "literal",
                "value": "Service 2"
              },
              "projectDistance": {
                "datatype": "http://www.w3.org/2001/XMLSchema#float",
                "type": "literal",
                "value": "54.321"
              }
            }
          ]
        }
      }
    """
)


def sparql_query_fuel(sum_of_fuel: float):
    return (
        """
        PREFIX hydrogen_nrmm: <https://w3id.org/hydrologiq/hydrogen/nrmm>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?producer ?producerName ?producerDailyOfftakeCapacity ?dispenser ?dispenserName ?dispenserLat ?dispenserLong ?dispenserFillingStationCapacity ?dispenserFillRate ?service ?serviceName
        where { 
            ?producer rdf:type hydrogen_nrmm:Hydrogen ;
                      rdfs:label ?producerName ;
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


SPARQL_QUERY_FUEL_RESPONSE = json.loads(
    """
{
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
      "serviceName"
    ]
  },
  "results": {
    "bindings": [
      {
        "producer": {
          "type": "uri",
          "value": "https://w3id.org/hydrologiq/hydrogen/nrmm312"
        },
        "producerName": {
          "type": "literal",
          "value": "Hydrogen Producer 1"
        },
        "producerDailyOfftakeCapacity": {
          "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
          "type": "literal",
          "value": "600"
        },
        "dispenser": {
          "type": "uri",
          "value": "https://w3id.org/hydrologiq/hydrogen/nrmm31"
        },
        "dispenserName": {
          "type": "literal",
          "value": "Dispensing Site 1"
        },
        "dispenserLat": {
          "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
          "type": "literal",
          "value": "123"
        },
        "dispenserLong": {
          "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
          "type": "literal",
          "value": "43.2"
        },
        "dispenserFillingStationCapacity": {
          "datatype": "http://www.w3.org/2001/XMLSchema#integer",
          "type": "literal",
          "value": "3"
        },
        "dispenserFillRate": {
          "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
          "type": "literal",
          "value": "10"
        },
        "service": {
          "type": "uri",
          "value": "https://w3id.org/hydrologiq/hydrogen/nrmm3"
        },
        "serviceName": {
          "type": "literal",
          "value": "Fuel Service 1"
        }
      }
    ]
  }
}
"""
)
