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

from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import List, Union

from pydantic import AnyHttpUrl, AwareDatetime, ConfigDict, Field, NaiveDatetime, field_validator
from rdflib.namespace import DCAT, DCTERMS, FOAF, URIRef

from sempyro import LiteralField
from sempyro.dcat import DCATDataset
from sempyro.foaf import Agent
from sempyro.namespaces import DCATv3
from sempyro.utils.validator_functions import date_handler, force_literal_field
from sempyro.vcard import VCard


class DatasetTheme(Enum):
    agri = URIRef("http://publications.europa.eu/resource/authority/data-theme/AGRI")
    econ = URIRef("http://publications.europa.eu/resource/authority/data-theme/ECON")
    educ = URIRef("http://publications.europa.eu/resource/authority/data-theme/EDUC")
    ener = URIRef("http://publications.europa.eu/resource/authority/data-theme/ENER")
    envi = URIRef("http://publications.europa.eu/resource/authority/data-theme/ENVI")
    gove = URIRef("http://publications.europa.eu/resource/authority/data-theme/GOVE")
    heal = URIRef("http://publications.europa.eu/resource/authority/data-theme/HEAL")
    intr = URIRef("http://publications.europa.eu/resource/authority/data-theme/INTR")
    just = URIRef("http://publications.europa.eu/resource/authority/data-theme/JUST")
    op_datpro = URIRef("http://publications.europa.eu/resource/authority/data-theme/OP_DATPRO")
    regi = URIRef("http://publications.europa.eu/resource/authority/data-theme/REGI")
    soci = URIRef("http://publications.europa.eu/resource/authority/data-theme/SOCI")
    tech = URIRef("http://publications.europa.eu/resource/authority/data-theme/TECH")
    tran = URIRef("http://publications.europa.eu/resource/authority/data-theme/TRAN")


class HRIDataset(DCATDataset):
    model_config = ConfigDict(
                              json_schema_extra={
                                  "$ontology": ["https://www.w3.org/TR/vocab-dcat-3/",
                                                "https://health-ri.atlassian.net/wiki/spaces/FSD/pages/121110529/Core+"
                                                "Metadata+Schema+Specification"],
                                  "$namespace": str(DCAT),
                                  "$IRI": DCAT.Dataset,
                                  "$prefix": "dcat"
                              }
                              )
    contact_point: Union[AnyHttpUrl, VCard] = Field(
        description="Relevant contact information for the cataloged resource. HRI mandatory",
        rdf_term=DCAT.contactPoint,
        rdf_type="uri")

    creator: List[Union[AnyHttpUrl, Agent]] = Field(
        description="The entity responsible for producing the resource. Resources of type foaf:Agent are "
                    "recommended as values for this property. HRI mandatory",
        rdf_term=DCTERMS.creator,
        rdf_type="uri")

    description: List[LiteralField] = Field(
        description="A free-text account of the resource. HRI mandatory",
        rdf_term=DCTERMS.description,
        rdf_type="literal"
    )
    issued: Union[str, datetime, date, AwareDatetime, NaiveDatetime] = Field(
        description="Date of formal issuance (e.g., publication) of the resource. HRI mandatory",
        rdf_term=DCTERMS.issued,
        rdf_type="datetime_literal"
    )
    identifier: Union[str, LiteralField] = Field(
        description="A unique identifier of the resource being described or cataloged. HRI mandatory",
        rdf_term=DCTERMS.identifier,
        rdf_type="rdfs_literal"
    )
    modified: Union[str, date, AwareDatetime, NaiveDatetime] = Field(
        description="Most recent date on which the resource was changed, updated or modified. HRI mandatory",
        rdf_term=DCTERMS.modified,
        rdf_type="datetime_literal"
    )
    publisher: List[Union[AnyHttpUrl, Agent]] = Field(
        description="The entity responsible for making the resource available. HRI mandatory",
        rdf_term=DCTERMS.publisher,
        rdf_type="uri"
    )
    theme: List[DatasetTheme] = Field(
        description="A main category of the resource. A resource can have multiple themes. HRI mandatory",
        rdf_term=DCAT.theme,
        rdf_type="uri"
    )
    title: List[LiteralField] = Field(
        description="A name given to the resource. HRI mandatory",
        rdf_term=DCTERMS.title,
        rdf_type="rdfs_literal"
    )
    type: List[AnyHttpUrl] = Field(
        default=None,
        description="The nature or genre of the resource. HRI recommended",
        rdf_term=DCTERMS.type,
        rdf_type="uri")
    license: AnyHttpUrl = Field(
        default=None,
        description="A legal document under which the resource is made available. HRI recommended",
        rdf_term=DCTERMS.license,
        rdf_type="uri"
    )
    distribution: List[AnyHttpUrl] = Field(
        default=None,
        description="An available distribution of the dataset. HRI recommended",
        rdf_term=DCAT.distribution,
        rdf_type="uri"
    )
    relation: List[AnyHttpUrl] = Field(
        default=None,
        description="connect dataset to the corresponding projects. HRI recommended",
        rdf_term=FOAF.Project,
        rdf_type="uri"
    )
    version: List[LiteralField] = Field(
        default=None,
        description="The version indicator (name or identifier) of a resource. HRI recommended",
        rdf_term=DCATv3.version,
        rdf_type="rdfs_literal"
    )
    in_series: List[AnyHttpUrl] = Field(
        default=None,
        description="A dataset series of which the dataset is part. HRI recommended",
        rdf_term=DCATv3.inSeries,
        rdf_type="uri"
    )

    @field_validator("title", "description", "keyword", mode="before")
    @classmethod
    def convert_to_literal(cls, value: List[Union[str, LiteralField]]) -> List[LiteralField]:
        return [force_literal_field(item) for item in value]

    @field_validator("issued", mode="before")
    @classmethod
    def date_validator(cls, value):
        return date_handler(value)


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "hri_dcat")
    HRIDataset.save_schema_to_file(Path(json_models_folder, "HRIDataset.json"), "json")
    HRIDataset.save_schema_to_file(Path(json_models_folder, "HRIDataset.yaml"), "yaml")
