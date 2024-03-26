from rdflib import DCAT, URIRef


class DCATv3(DCAT):
    """Extends DCAT namespace with properties added in v3"""
    # http://www.w3.org/2002/07/owl#ObjectProperty
    version: URIRef
    previousVersion: URIRef
    hasCurrentVersion: URIRef
    first: URIRef
    last: URIRef
    prev: URIRef
    inSeries: URIRef

    # http://www.w3.org/2002/07/owl#Class
    DatasetSeries: URIRef
