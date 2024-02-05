from rdflib import DCAT, URIRef


class DCATv3(DCAT):
    """Extends DCAT namespace with properties added in v3"""
    version: URIRef
    previousVersion: URIRef
    hasCurrentVersion: URIRef
    first: URIRef
    last: URIRef
    prev: URIRef
    inSeries: URIRef
