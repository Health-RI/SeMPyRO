from abc import ABCMeta
import logging
import re

from datetime import date
from enum import Enum
from pydantic import ConfigDict, Field, AnyHttpUrl, AnyUrl, field_validator, AwareDatetime, \
    NaiveDatetime
from typing import List, Union, Any
from rdflib import Namespace, URIRef
from rdflib.namespace import DCAT, DCTERMS, FOAF, PROV, ODRL2
from pydantic.networks import validate_email

from dcat.rdf_model import RDFModel, LiteralField
from namespaces.ADMS import ADMS, ADMSStatus
from namespaces.DCATv3 import DCATv3

logger = logging.getLogger("__name__")

VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")


class Status(Enum):
    Completed = ADMSStatus.Completed
    Deprecated = ADMSStatus.Deprecated
    UnderDevelopment = ADMSStatus.UnderDevelopment
    Withdrawn = ADMSStatus.Withdrawn


class VCard(RDFModel):
    model_config = ConfigDict(title=VCARD)
    # todo bind namespace at serialization

    hasEmail: AnyUrl = Field(default=None,
                             description="The email address as a mailto URI",
                             rdf_term=VCARD.hasEmail,
                             rdf_type="uri"
                             )
    full_name: str = Field(default=None,
                           description="The full name of the object (as a single string). This is the only mandatory "
                                       "property.",
                           rdf_term=VCARD.fn,
                           rdf_type="rdfs_literal"
                           )
    hasUID: AnyHttpUrl = Field(description="A unique identifier for the object",
                               rdf_term=VCARD.hasUID,
                               rdf_type="uri"
                               )

    @field_validator("hasEmail", mode="before")
    @classmethod
    def _validate_email(cls, value: Union[str, AnyUrl]) -> AnyUrl:
        """
        Checks if provided value is a valid email or mailto URI, fulfills an email to mailto URI
        """
        mail_part = value
        if value.startswith("mailto:"):
            mail_part = re.split(":|\//", value)[-1]
        mail_part = validate_email(mail_part)[1]
        return AnyUrl(f"mailto://{mail_part}")


class Agent(RDFModel):
    model_config = ConfigDict(title=FOAF.Agent)
    name: List[Union[str, LiteralField]] = Field(description="A name of the agent",
                                                 min_items=1,
                                                 rdf_term=FOAF.name,
                                                 rdf_type="rdfs_literal"
                                                 )
    identifier: Union[str, LiteralField] = Field(description="A unique identifier of the agent.",
                                                 rdf_term=DCTERMS.identifier,
                                                 rdf_type="rdfs_literal")


class ODRLPolicy(RDFModel):
    model_config = ConfigDict(title=ODRL2.Policy)
    conflict: Any = Field(default=None)
    permission: Any = Field(default=None)
    prohibition: Any = Field(default=None)
    inheritFrom: Any = Field(default=None)
    profile: Any = Field(default=None)
    obligation: Any = Field(default=None)
    uid: Any = Field(default=None)
    relation: Any = Field(default=None)
    target: Any = Field(default=None)
    function: Any = Field(default=None)
    action: Any = Field(default=None)
    constraint: Any = Field(default=None)
    assignee: Any = Field(default=None)
    assigner: Any = Field(default=None)


class AccessRights(Enum):
    public = "public"
    restricted = "restricted",
    non_public = "non-public"


class DCATResource(RDFModel, metaclass=ABCMeta):
    """Resource published or curated by a single agent. Abstract class"""
    model_config = ConfigDict(arbitrary_types_allowed=True, use_enum_values=True)
    access_rights: Enum = Field(default=None,
                                description="Information about who can access the resource or an indication of its "
                                            "security status.",
                                rdf_term=DCTERMS.accessRights,
                                rdf_type="literal")
    conforms_to: AnyHttpUrl = Field(default=None,
                                    description="An established standard to which the described resource conforms.",
                                    rdf_term=DCTERMS.conformsTo,
                                    rdf_type="uri"
                                    )
    contact_point: List[Union[AnyHttpUrl, VCard, Agent]] = Field(default=None,
                                                                 description="Relevant contact information for the "
                                                                             "cataloged resource. Use of vCard is "
                                                                             "recommended",
                                                                 rdf_term=DCAT.contactPoint,
                                                                 rdf_type="uri")
    creator: List[Union[AnyHttpUrl, VCard, Agent]] = Field(default=None,
                                                           description="The entity responsible for producing the "
                                                                       "resource. Resources of type foaf:Agent are "
                                                                       "recommended as values for this property.",
                                                           rdf_term=DCTERMS.creator,
                                                           rdf_type="uri")
    description: List[LiteralField] = Field(description="A free-text account of the resource.",
                                            min_items=1,
                                            rdf_term=DCTERMS.description,
                                            rdf_type="literal"
                                            )
    has_part: AnyHttpUrl = Field(default=None,
                                 description="A related resource that is included either physically or logically in "
                                             "the described resource.",
                                 rdf_term=DCTERMS.hasPart,
                                 rdf_type="uri")
    has_policy: ODRLPolicy = Field(default=None,
                                   description="An ODRL conformant policy expressing the rights associated with the "
                                               "resource.",
                                   rdf_term=ODRL2.hasPolicy,
                                   rdf_type=ODRLPolicy
                                   )
    identifier: Union[str, LiteralField] = Field(description="A unique identifier of the resource being described or cataloged.",
                                                 rdf_term=DCTERMS.identifier,
                                                 rdf_type="rdfs_literal")
    is_referenced_by: AnyHttpUrl = Field(default=None,
                                         description="A related resource, such as a publication, that references, "
                                                     "cites, or otherwise points to the cataloged resource.",
                                         rdf_term=DCTERMS.isReferencedBy,
                                         rdf_type="uri"
                                         )
    keyword: List[LiteralField] = Field(default=None,
                                        description="A keyword or tag describing the resource.",
                                        alias="tag",
                                        rdf_term=DCAT.keyword,
                                        rdf_type="rdfs_literal")
    landing_page: List[AnyHttpUrl] = Field(default=None,
                                           description="A Web page that can be navigated to in a Web browser to gain "
                                                       "access to the catalog, a dataset, its distributions and/or "
                                                       "additional information.",
                                           rdf_term=DCAT.landingPage,
                                           rdf_type="uri")
    license: AnyHttpUrl = Field(default=None,
                                description="A legal document under which the resource is made available.",
                                rdf_term=DCTERMS.license,
                                rdf_type="uri"
                                )
    language: List[AnyHttpUrl] = Field(default=None,
                                       description="A language of the resource. This refers to the natural language "
                                                   "used for textual metadata (i.e., titles, descriptions, etc.) of "
                                                   "a cataloged resource (i.e., dataset or service) or the textual "
                                                   "values of a dataset distribution",
                                       rdf_term=DCTERMS.language,
                                       rdf_type="uri"
                                       )
    relation: List[AnyHttpUrl] = Field(default=None,
                                       description="A resource with an unspecified relationship to the cataloged "
                                                   "resource.",
                                       rdf_term=DCTERMS.relation,
                                       rdf_type="uri"
                                       )
    rights: Any = Field(default=None,
                        description="Information about rights held in and over the distribution."
                                    "Recommended practice is to refer to a rights statement with a URI. "
                                    "If this is not possible or feasible, a literal value (name, label, or short text) "
                                    "may be provided.",
                        rdf_term=DCTERMS.rights,
                        rdf_type="rdfs_literal")  # todo deal with multiple types
    qualified_relation: List[AnyHttpUrl] = Field(default=None,
                                                 description="Link to a description of a relationship with another "
                                                             "resource",
                                                 rdf_term=DCAT.qualifiedRelation,
                                                 rdf_type="uri"
                                                 )
    publisher: List[Union[AnyHttpUrl, Agent]] = Field(default=None,
                                                      description="The entity responsible for making the resource "
                                                                  "available.",
                                                      rdf_term=DCTERMS.publisher,
                                                      rdf_type="uri"
                                                      )
    release_date: Union[date, AwareDatetime, NaiveDatetime] = Field(default=None,
                                                                    description="Date of formal issuance "
                                                                                "(e.g., publication) of the resource.",
                                                                    rdf_term=DCTERMS.issued,
                                                                    rdf_type="rdfs_literal")
    # todo date to literal: rdfs:Literal encoded using the relevant ISO 8601 Date and Time compliant string [DATETIME] 
    #  and typed using the appropriate XML Schema datatype [XMLSCHEMA11-2] (xsd:gYear, xsd:gYearMonth, xsd:date, or xsd:dateTime).
    theme: List[URIRef] = Field(default=None,
                                description="A main category of the resource. A resource can have multiple themes.",
                                alias="category",
                                rdf_term=DCAT.theme,
                                rdf_type="uri")
    title: List[LiteralField] = Field(description="A name given to the resource.",
                                      rdf_term=DCTERMS.title,
                                      rdf_type="rdfs_literal"
                                      )
    type: List[AnyHttpUrl] = Field(default=None,
                                   description="The nature or genre of the resource.",
                                   alias="genre",
                                   rdf_term=DCTERMS.type,
                                   rdf_type="uri")
    update_date: Union[str, date, AwareDatetime, NaiveDatetime] = Field(
        default=None,
        description="Most recent date on which the resource was changed, updated or modified.",
        alias="modification_date",
        rdf_term=DCTERMS.modified,
        rdf_type="rdfs_literal"
    )  # todo date format
    qualified_attribution: List[AnyHttpUrl] = Field(
        default=None,
        description="Link to an Agent having some form of responsibility for the resource",
        rdf_term=PROV.qualifiedAttribution,
        rdf_type="uri"
    )
    has_current_version: AnyHttpUrl = Field(
        default=None,
        description="This resource has a more specific, versioned resource with equivalent content [PAV].",
        rdf_term=DCATv3.hasCurrentVersion,
        rdf_type="uri"
    )
    has_version: List[AnyHttpUrl] = Field(
        default=None,
        description="This resource has a more specific, versioned resource",
        rdf_term=DCTERMS.hasVersion,
        rdf_type="uri"
    )
    previous_version: AnyHttpUrl = Field(default=None,
                                         description="The previous version of a resource in a lineage [PAV].",
                                         rdf_term=DCATv3.previousVersion,
                                         rdf_type="uri"
                                         )
    replaces: AnyHttpUrl = Field(
        default=None,
        description="A related resource that is supplanted, displaced, or superseded by the described resource",
        rdf_term=DCTERMS.replaces,
        rdf_type="uri"
    )
    status: Status = Field(default=None,
                           description="The status of the resource in the context of a particular workflow process "
                                       "[VOCAB-ADMS].",
                           rdf_term=ADMS.status,
                           rdf_type="uri"
                           )
    version: List[LiteralField] = Field(
        default=None,
        description="The version indicator (name or identifier) of a resource.",
        rdf_term=DCATv3.version,
        rdf_type="rdfs_literal"
    )
    version_notes: List[LiteralField] = Field(
        default=None,
        description="A description of changes between this version and the previous version of the resource "
                    "[VOCAB-ADMS].",
        rdf_term=ADMS.versionNotes,
        rdf_type="rdfs_literal")

    first: AnyHttpUrl = Field(
        default=None,
        description="The first resource in an ordered collection or series of resources, to which the current resource "
                    "belongs.",
        rdf_term=DCATv3.first,
        rdf_type="uri"
    )
    last: AnyHttpUrl = Field(
        default=None,
        description="The last resource in an ordered collection or series of resources, to which the current resource "
                    "belongs.",
        rdf_term=DCATv3.last,
        rdf_type="uri"
    )
    previous: List[AnyHttpUrl] = Field(
        default=None,
        description="The previous resource (before the current one) in an ordered collection or series of resources.",
        rdf_term=DCATv3.prev,
        rdf_type="uri"
    )

    @field_validator("title", "description", "keyword", "version", "version_notes", mode="before")
    @classmethod
    def force_literal_field(cls, value: List[Union[str, LiteralField]]) -> List[LiteralField]:
        """
        In case values are provided as a strings, convert to LiteralField object with none as datatype and language
        """
        new_list = []
        for item in value:
            if isinstance(item, str):
                new_list.append(LiteralField(value=item))
            else:
                new_list.append(item)
        return new_list

    @classmethod
    def to_graph(cls):
        pass
