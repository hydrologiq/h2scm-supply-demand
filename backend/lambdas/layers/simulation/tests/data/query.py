import json


def sparql_query_logistic(minStorage: int):
    return (
        """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?storage ?storageName ?storageAvailableQuantity ?storageCapacity ?vehicle ?vehicleName ?vehicleAvailableQuantity ?vehicleTransportDistance ?service ?serviceName ?price ?priceMonetaryValue
where {
    ?storage rdf:type hydrogen_nrmm:TubeTrailer ;
             rdfs:label ?storageName ;
             hydrogen_nrmm:availableQuantity ?storageAvailableQuantity ;
             hydrogen_nrmm:capacity ?storageCapacity ;.
    FILTER(?storageCapacity >= """
        + f"{minStorage}"
        + """)
    ?vehicle hydrogen_nrmm:carries hydrogen_nrmm:TubeTrailer ;
             rdfs:label ?vehicleName ;
             hydrogen_nrmm:availableQuantity ?vehicleAvailableQuantity ;
             hydrogen_nrmm:transportDistance ?vehicleTransportDistance ;.
    ?service rdf:type hydrogen_nrmm:LogisticService;
             rdfs:label ?serviceName ;
             hydrogen_nrmm:includes ?storage;
             hydrogen_nrmm:includes ?vehicle;
             hydrogen_nrmm:typicalPricing ?quote;.
    ?quote hydrogen_nrmm:price ?price;.
    ?price hydrogen_nrmm:monetaryValue ?priceMonetaryValue;
             hydrogen_nrmm:unit ?priceUnit;.
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
            "storageAvailableQuantity",
            "storageCapacity",
            "vehicle",
            "vehicleName",
            "vehicleAvailableQuantity",
            "vehicleTransportDistance",
            "service",
            "serviceName",
            "price",
            "priceMonetaryValue"
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
              "price": {
                "type": "uri",
                "value": "https://w3id.org/hydrologiq/hydrogen/nrmm12345"
              },
              "priceMonetaryValue": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": "80.0"
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
              "price": {
                "type": "uri",
                "value": "https://w3id.org/hydrologiq/hydrogen/nrmm214"
              },
              "priceMonetaryValue": {
                "datatype": "http://www.w3.org/2001/XMLSchema#decimal",
                "type": "literal",
                "value": "40.0"
              }
            }
          ]
        }
      }
    """
)
