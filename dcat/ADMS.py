from rdflib.namespace import DefinedNamespace, Namespace
from rdflib import URIRef


class ADMS(DefinedNamespace):
    """
    Namespace for ADMS Vocabulary

    ADMS, the Asset Description Metadata Schema, is a vocabulary for describing semantic assets (or just 'Assets'), 
    defined as highly reusable metadata (e.g. XML schemata, generic data models) and reference data (e.g. code lists, 
    taxonomies, dictionaries, vocabularies).

    Generated based on https://uri.semic.eu/w3c/ns/adms.ttl 
    Date: 2024-02-26 05
    """

    # http://www.w3.org/2002/07/owl#ObjectProperty
    identifier: URIRef  # Links a resource to an adms:Identifier class.
    includedAsset: URIRef  # An Asset that is contained in the Asset being described, e.g. when there are several vocabularies defined in a single document.
    interoperabilityLevel: URIRef  # The interoperability level for which the Asset is relevant.
    last: URIRef  # A link to the current or latest version of the Asset.
    next: URIRef  # A link to the next version of the Asset.
    prev: URIRef  # A link to the previous version of the Asset.
    representationTechnique: URIRef  # More information about the format in which an Asset Distribution is released. This is different from the file format as, for example, a ZIP file (file format) could contain an XML schema (representation technique).
    sample: URIRef  # Links to a sample of an Asset (which is itself an Asset).
    schemaAgency: URIRef  # The name of the agency that issued the identifier.
    status: URIRef  # The status of the Asset in the context of a particular workflow process.
    supportedSchema: URIRef  # A schema according to which the Asset Repository can provide data about its content, e.g. ADMS.
    translation: URIRef  # Links Assets that are translations of each other.
    versionNotes: URIRef  # A description of changes between this version and the previous version of the Asset.

    # http://www.w3.org/2002/07/owl#Class>
    Asset: URIRef  # An abstract entity that reflects the intellectual content of the asset and represents those characteristics of the asset that are independent of its physical embodiment. This abstract entity combines the FRBR entities work (a distinct intellectual or artistic creation) and expression (the intellectual or artistic realization of a work)
    AssetDistribution: URIRef  # A particular physical embodiment of an Asset, which is an example of the FRBR entity manifestation (the physical embodiment of an expression of a work).
    AssetRepository: URIRef  # A system or service that provides facilities for storage and maintenance of descriptions of Assets and Asset Distributions, and functionality that allows users to search and access these descriptions. An Asset Repository will typically contain descriptions of several Assets and related Asset Distributions.
    Identifier: URIRef  # This is based on the UN/CEFACT Identifier class.

    _NS = Namespace("http://www.w3.org/ns/adms#")


class ADMSStatus(DefinedNamespace):
    """"""
    Completed: URIRef
    Deprecated: URIRef
    UnderDevelopment: URIRef
    Withdrawn: URIRef

    _NS = Namespace("http://purl.org/adms/status/")
