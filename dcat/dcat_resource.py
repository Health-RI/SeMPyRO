from abc import ABCMeta
import logging
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from rdflib import DCAT, DCTERMS, Dataset
from typing import List, Optional, Union
from pydantic import BaseModel, Field, validator, AwareDatetime, NaiveDatetime
from rdflib import BNode, Graph, Namespace, URIRef, Literal
from rdflib.namespace import DCAT, DCTERMS, RDF, XSD, RDFS, TIME
from typing_extensions import Annotated

from dcat_time_models import Temporal

from enum import Enum

from datetime import date, datetime, time

from dcat.DCATv3 import DCATv3

VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")


RDF_KEY = "rdf_term"
RDF_TYPE_KEY = "rdf_type"


logger = logging.getLogger("__name__")


class VCard(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    full_name: Literal = Field(default=None)
    uid: URIRef
    # todo extend?
    # email: EmailStr = Field(default=None)


class AccessRights(Enum):
    public = "public"
    restricted = "restricted",
    non_public = "non-public"


class RDFTypes(Enum):
    def __str__(self):
        return str(self.value)
    literal = Literal
    uri = URIRef


class DCATResource(BaseModel, metaclass=ABCMeta):
    model_config = ConfigDict(arbitrary_types_allowed=True, use_enum_values=True)
    access_rights: Enum = Field(default=None,
                                description="Information about who can access the resource or an indication of its "
                                            "security status.",
                                rdf_term=DCTERMS.accessRights)
    conforms_to: str = Field(default=None,
                             description="An established standard to which the described resource conforms.",
                             rdf_term=DCTERMS.conformsTo,
                             rdf_type="uri"
                             )
    contact_point: Union[List[str], List[VCard]] = Field(default=None,
                                                         description="Relevant contact information for the cataloged"
                                                                     "resource. Use of vCard is recommended",
                                                         rdf_term=DCAT.contactPoint,
                                                         rdf_type="uri")
    creator: Union[List[str], List[VCard]] = Field(default=None,
                                                   description="The entity responsible for producing the resource.",
                                                   rdf_term=DCTERMS.creator,
                                                   rdf_type="uri")
    description: List[str] = Field(description="",
                                   min_items=1,
                                   rdf_term=DCTERMS.description,
                                   rdf_type="literal"
                                   )
    has_part: URIRef = Field(default=None,
                             description="",
                             rdf_term=DCTERMS.hasPart,
                             rdf_type="uri")
    # has_policy: str = Field(default=None, description="")
    identifier: URIRef = Field(
                                description="A unique identifier of the resource being described or cataloged.",
                                rdf_term=DCTERMS.identifier,
                                rdf_type="uri"
                               )  # in dcat it is Literal which becomes a part of a URI
    is_referenced_by: URIRef = Field(default=None,
                                     description="",
                                     alias="tag",
                                     rdf_term=DCTERMS.isReferencedBy,
                                     rdf_type="uri"
                                     )
    keyword: List[Literal] = Field(default=None, description="", alias="tag", rdf_term=DCAT.keyword)
    landing_page: URIRef = Field(default=None,
                                 description="A Web page that can be navigated to in a Web browser to gain access to"
                                             "the catalog, a dataset, its distributions and/or additional information.",
                                 rdf_term=DCAT.landingPage,
                                 rdf_type="uri")
    license: URIRef = Field(default=None,
                            description="A legal document under which the resource is made available.",
                            rdf_term=DCTERMS.license,
                            rdf_type="uri"
                            )
    # language: str = Field(default=None, description="")
    # relation: str = Field(default=None, description="")
    # rights: str = Field(default=None, description="")
    # qualified_relation: str = Field(default=None, description="")
    publisher: List[URIRef] = Field(default=None,
                                    description="The entity responsible for making the resource available.",
                                    rdf_term=DCTERMS.publisher
                                    )
    release_date: Literal = Field(default=None,
                                  description="Date of formal issuance (e.g., publication) of the resource.",
                                  rdf_term=DCTERMS.issued) # todo date to literal: rdfs:Literal encoded using the relevant ISO 8601 Date and Time compliant string [DATETIME] and typed using the appropriate XML Schema datatype [XMLSCHEMA11-2] (xsd:gYear, xsd:gYearMonth, xsd:date, or xsd:dateTime).
    theme: List[URIRef] = Field(default=None, description="", alias="category", rdf_type="uri")
    title: Literal = Field(description="A name given to the resource.",
                           rdf_term=DCTERMS.title)
    # type: # str = Field(default=None, description="", alias="genre")
    # update_date: str = Field(default=None, description="", alias="modification_date")
    # qualified_attribution: str = Field(default=None, description="")
    # has_current_version: str = Field(default=None, description="")
    has_version: URIRef = Field(
                                default=None,
                                description="This resource has a more specific, versioned resource",
                                rdf_term=DCTERMS.hasVersion,
                                rdf_type="uri"
                                )
    # previous_version: str = Field(default=None, description="")
    # replaces: str = Field(default=None, description="")
    # status: str = Field(default=None, description="")
    version: Literal = Field(default=None,
                             description="The version indicator (name or identifier) of a resource.",
                             rdf_term=DCATv3.version)
    # version_notes: str = Field(default=None, description="")
    # first: str = Field(default=None, description="")
    # last: str = Field(default=None, description="")
    # previous: str = Field(default=None, description="", alias="tag", rdf_term=DCAT.previousVersion) #todo add to namespace

    def to_graph(cls):
        pass
