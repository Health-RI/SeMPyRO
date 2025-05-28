# Copyright 2024 Stichting Health-RI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from abc import ABCMeta
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import List, Union, Optional, ClassVar, Set

from pydantic import AnyHttpUrl, AwareDatetime, ConfigDict, Field, NaiveDatetime, field_validator
from rdflib import DCAT, DCTERMS, ODRL2, PROV, URIRef

from sempyro import LiteralField, RDFModel
from sempyro.foaf import Agent
from sempyro.geo import Location
from sempyro.namespaces import ADMS, ADMSStatus, DCATv3
from sempyro.odrl import ODRLPolicy
from sempyro.time import PeriodOfTime
from sempyro.utils.validator_functions import date_handler, convert_to_literal
from sempyro.vcard import VCard

logger = logging.getLogger("__name__")


class Status(Enum):
    Completed = ADMSStatus.Completed
    Deprecated = ADMSStatus.Deprecated
    UnderDevelopment = ADMSStatus.UnderDevelopment
    Withdrawn = ADMSStatus.Withdrawn


class AccessRights(Enum):
    public = URIRef("http://publications.europa.eu/resource/authority/access-right/PUBLIC")
    restricted = URIRef("http://publications.europa.eu/resource/authority/access-right/RESTRICTED")
    non_public = URIRef("http://publications.europa.eu/resource/authority/access-right/NON_PUBLIC")


class DCATResource(RDFModel, metaclass=ABCMeta):
    """Resource published or curated by a single agent. Abstract class"""
    model_config = ConfigDict(arbitrary_types_allowed=True,
                              use_enum_values=True,
                              json_schema_extra={
                                  "$ontology": "https://www.w3.org/TR/vocab-dcat-3/",
                                  "$namespace": str(DCAT),
                                  "$IRI": DCAT.Resource,
                                  "$prefix": "dcat"
                              }
                              )
    access_rights: AccessRights = Field(
        default=None,
        description="Information about who can access the resource or an indication of its security status.",
        json_schema_extra={
            "rdf_term": DCTERMS.accessRights,
            "rdf_type": "uri"
        }
    )
    conforms_to: AnyHttpUrl = Field(
        default=None,
        description="An established standard to which the described resource conforms.",
        json_schema_extra={
            "rdf_term": DCTERMS.conformsTo,
            "rdf_type": "uri"
        }
    )
    contact_point: List[Union[AnyHttpUrl, VCard, Agent]] = Field(
        default=None,
        description="Relevant contact information for the cataloged resource. Use of vCard is recommended",
        json_schema_extra={
            "rdf_term": DCAT.contactPoint,
            "rdf_type": "uri"
        }
    )
    creator: List[Union[AnyHttpUrl, VCard, Agent]] = Field(
        default=None,
        description="The entity responsible for producing the resource. Resources of type foaf:Agent are "
                    "recommended as values for this property.",
        json_schema_extra={
            "rdf_term": DCTERMS.creator,
            "rdf_type": "uri"
        }
    )
    description: List[Union[LiteralField, str]] = Field(
        description="An account of the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.description,
            "rdf_type": "rdfs_literal"
        }
    )
    has_part: List[AnyHttpUrl] = Field(
        default=None,
        description="A related resource that is included either physically or logically in the described resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.hasPart,
            "rdf_type": "uri"
        }
    )
    has_policy: ODRLPolicy = Field(
        default=None,
        description="An ODRL conformant policy expressing the rights associated with the resource.",
        json_schema_extra={
            "rdf_term": ODRL2.hasPolicy,
            "rdf_type": "uri"
        }
    )
    identifier: List[Union[str, LiteralField]] = Field(
        default=None,
        description="A unique identifier of the resource being described or cataloged.",
        json_schema_extra={
            "rdf_term": DCTERMS.identifier,
            "rdf_type": "rdfs_literal"
        }
    )
    is_referenced_by: List[AnyHttpUrl] = Field(
        default=None,
        description="A related resource, such as a publication, that references, cites, or otherwise points to the "
                    "cataloged resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.isReferencedBy,
            "rdf_type": "uri"
        }
    )
    keyword: List[LiteralField] = Field(
        default=None,
        description="A keyword or tag describing the resource.",
        json_schema_extra={
            "rdf_term": DCAT.keyword,
            "rdf_type": "rdfs_literal"
        }
    )
    landing_page: List[AnyHttpUrl] = Field(
        default=None,
        description="A Web page that can be navigated to in a Web browser to gain access to the catalog, a dataset, "
                    "its distributions and/or additional information.",
        json_schema_extra={
            "rdf_term": DCAT.landingPage,
            "rdf_type": "uri"
        }
    )
    license: Optional[AnyHttpUrl] = Field(
        default=None,
        description="A legal document under which the resource is made available.",
        json_schema_extra={
            "rdf_term": DCTERMS.license,
            "rdf_type": "uri"
        }
    )
    language: List[AnyHttpUrl] = Field(
        default=None,
        description="A language of the resource. This refers to the natural language used for textual metadata "
                    "(i.e., titles, descriptions, etc.) of a cataloged resource (i.e., dataset or service) or the "
                    "textual values of a dataset distribution",
        json_schema_extra={
            "rdf_term": DCTERMS.language,
            "rdf_type": "uri"
        }
    )
    relation: List[AnyHttpUrl] = Field(
        default=None,
        description="A resource with an unspecified relationship to the cataloged resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.relation,
            "rdf_type": "uri"
        }
    )
    rights: Union[LiteralField, AnyHttpUrl] = Field(
        default=None,
        description="Information about rights held in and over the distribution. Recommended practice is to refer to "
                    "a rights statement with a URI. If this is not possible or feasible, a literal value (name, label, "
                    "or short text) may be provided.",
        json_schema_extra={
            "rdf_term": DCTERMS.rights,
            "rdf_type": "uri"
        }
    )
    qualified_relation: List[AnyHttpUrl] = Field(
        default=None,
        description="Link to a description of a relationship with another resource",
        json_schema_extra={
            "rdf_term": DCAT.qualifiedRelation,
            "rdf_type": "uri"
        }
    )
    publisher: List[Union[AnyHttpUrl, Agent]] = Field(
        default=None,
        description="The entity responsible for making the resource available.",
        json_schema_extra={
            "rdf_term": DCTERMS.publisher,
            "rdf_type": "uri"
        }
    )
    release_date: Union[str, datetime, date, AwareDatetime, NaiveDatetime] = Field(
        default=None,
        description="Date of formal issuance (e.g., publication) of the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.issued,
            "rdf_type": "datetime_literal"
        }
    )
    theme: List[AnyHttpUrl] = Field(
        default=None,
        description="A main category of the resource. A resource can have multiple themes.",
        json_schema_extra={
            "rdf_term": DCAT.theme,
            "rdf_type": "uri"
        }
    )
    title: List[Union[LiteralField, str]] = Field(
        description="A name given to the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.title,
            "rdf_type": "rdfs_literal"
        }
    )
    type: List[AnyHttpUrl] = Field(
        default=None,
        description="The nature or genre of the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.type,
            "rdf_type": "uri"
        }
    )
    modification_date: Union[str, date, AwareDatetime, NaiveDatetime] = Field(
        default=None,
        description="Most recent date on which the resource was changed, updated or modified.",
        json_schema_extra={
            "rdf_term": DCTERMS.modified,
            "rdf_type": "datetime_literal"
        }
    )
    qualified_attribution: List[AnyHttpUrl] = Field(
        default=None,
        description="Link to an Agent having some form of responsibility for the resource",
        json_schema_extra={
            "rdf_term": PROV.qualifiedAttribution,
            "rdf_type": "uri"
        }
    )
    has_current_version: AnyHttpUrl = Field(
        default=None,
        description="This resource has a more specific, versioned resource with equivalent content [PAV].",
        json_schema_extra={
            "rdf_term": DCATv3.hasCurrentVersion,
            "rdf_type": "uri"
        }
    )
    has_version: List[AnyHttpUrl] = Field(
        default=None,
        description="This resource has a more specific, versioned resource",
        json_schema_extra={
            "rdf_term": DCTERMS.hasVersion,
            "rdf_type": "uri"
        }
    )
    previous_version: AnyHttpUrl = Field(
        default=None,
        description="The previous version of a resource in a lineage [PAV].",
        json_schema_extra={
            "rdf_term": DCATv3.previousVersion,
            "rdf_type": "uri"
        }
    )
    replaces: AnyHttpUrl = Field(
        default=None,
        description="A related resource that is supplanted, displaced, or superseded by the described resource",
        json_schema_extra={
            "rdf_term": DCTERMS.replaces,
            "rdf_type": "uri"
        }
    )
    status: Status = Field(
        default=None,
        description="The status of the resource in the context of a particular workflow process [VOCAB-ADMS].",
        json_schema_extra={
            "rdf_term": ADMS.status,
            "rdf_type": "uri"
        }
    )

    version: Union[str, LiteralField] = Field(
        default=None,
        description="The version indicator (name or identifier) of a resource.",
        json_schema_extra={
            "rdf_term": DCATv3.version,
            "rdf_type": "rdfs_literal"
        }
    )
    version_notes: List[Union[str, LiteralField]] = Field(
        default=None,
        description="A description of changes between this version and the previous version of the resource "
                    "[VOCAB-ADMS].",
        json_schema_extra={
            "rdf_term": ADMS.versionNotes,
            "rdf_type": "rdfs_literal"
        }
    )
    first: AnyHttpUrl = Field(
        default=None,
        description="The first resource in an ordered collection or series of resources, to which the current resource "
                    "belongs.",
        json_schema_extra={
            "rdf_term": DCATv3.first,
            "rdf_type": "uri"
        }
    )
    last: AnyHttpUrl = Field(
        default=None,
        description="The last resource in an ordered collection or series of resources, to which the current resource "
                    "belongs.",
        json_schema_extra={
            "rdf_term": DCATv3.last,
            "rdf_type": "uri"
        }
    )
    previous: List[AnyHttpUrl] = Field(
        default=None,
        description="The previous resource (before the current one) in an ordered collection or series of resources.",
        json_schema_extra={
            "rdf_term": DCATv3.prev,
            "rdf_type": "uri"
        }
    )
    temporal_coverage: List[PeriodOfTime] = Field(
        default=None,
        description="The temporal period that the dataset covers.",
        json_schema_extra={
            "rdf_term": DCTERMS.temporal,
            "rdf_type": DCTERMS.PeriodOfTime
        }
    )
    geographical_coverage: List[Union[AnyHttpUrl, Location]] = Field(
        default=None,
        description="The geographical area covered by the dataset.",
        json_schema_extra={
            "rdf_term": DCTERMS.spatial,
            "rdf_type": "uri"
        }
    )

    _validate_literal_fields: ClassVar[Set[str]] = {"title", "description", "keyword", "version", "version_notes"}

    @field_validator(*_validate_literal_fields, mode="before")
    @classmethod
    def validate_literal(cls, value: List[Union[str, LiteralField]]) -> List[LiteralField]:
        return convert_to_literal(value)

    @field_validator("release_date", "modification_date", mode="before")
    @classmethod
    def date_validator(cls, value):
        return date_handler(value)


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "dcat")
    DCATResource.save_schema_to_file(Path(json_models_folder, "DCATResource.json"), "json")
    DCATResource.save_schema_to_file(Path(json_models_folder, "DCATResource.yaml"), "yaml")
