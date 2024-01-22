from rdflib import DCAT, URIRef


class DCATv3(DCAT):
    """Extends DCAT namespace with parameters added in v3"""
    version: URIRef
