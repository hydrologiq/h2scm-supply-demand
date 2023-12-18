def tube_trailer_availability():
  return """
        PREFIX hydrogen_nrmm: <https://w3id.org/hydrologiq/hydrogen/nrmm>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        select ?s ?trailerCapacity ?avlQuant ?service where { 
            ?s rdf:type hydrogen_nrmm:TubeTrailer ;
                hydrogen_nrmm:availableQuantity ?avlQuant ;
                hydrogen_nrmm:capacity ?trailerCapacity ;.
            ?service hydrogen_nrmm:includes ?s
            FILTER (?avlQuant >= 1)
        }
    """

def adr_truck_availability():
  return """
        PREFIX hydrogen_nrmm: <https://w3id.org/hydrologiq/hydrogen/nrmm>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        select ?s ?avlQuant ?service where { 
            ?s hydrogen_nrmm:carries hydrogen_nrmm:TubeTrailer ;
            hydrogen_nrmm:availableQuantity ?avlQuant ;.
            ?service hydrogen_nrmm:includes ?s
            FILTER (?avlQuant >= 1)
        }
    """
