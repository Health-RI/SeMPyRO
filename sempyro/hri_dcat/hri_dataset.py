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
from pathlib import Path
from pydantic import Field, AnyHttpUrl, ConfigDict, AwareDatetime, NaiveDatetime, field_validator
from rdflib.namespace import DCAT, DCTERMS, FOAF
from typing import List, Union

from sempyro.foaf import Agent
from sempyro import RDFModel, LiteralField
from sempyro.namespaces import DCATv3
from sempyro.utils.validator_functions import date_handler, force_literal_field


class HRIDataset(RDFModel):
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
    contact_point: List[Union[AnyHttpUrl, Agent]] = Field(
        description="Relevant contact information for the cataloged resource.",
        rdf_term=DCAT.contactPoint,
        rdf_type="uri")

    creator: List[Union[AnyHttpUrl, Agent]] = Field(
        description="The entity responsible for producing the resource. Resources of type foaf:Agent are "
                    "recommended as values for this property.",
        rdf_term=DCTERMS.creator,
        rdf_type="uri")

    description: List[LiteralField] = Field(
        description="A free-text account of the resource.",
        rdf_term=DCTERMS.description,
        rdf_type="literal"
    )
    issued: Union[str, datetime, date, AwareDatetime, NaiveDatetime] = Field(
        description="Date of formal issuance (e.g., publication) of the resource.",
        rdf_term=DCTERMS.issued,
        rdf_type="datetime_literal"
    )
    identifier: Union[str, LiteralField] = Field(
        description="A unique identifier of the resource being described or cataloged.",
        rdf_term=DCTERMS.identifier,
        rdf_type="xsd:string")
    modified: Union[str, date, AwareDatetime, NaiveDatetime] = Field(
        description="Most recent date on which the resource was changed, updated or modified.",
        rdf_term=DCTERMS.modified,
        rdf_type="datetime_literal"
    )
    publisher: List[Union[AnyHttpUrl, Agent]] = Field(
        description="The entity responsible for making the resource available.",
        rdf_term=DCTERMS.publisher,
        rdf_type="uri"
    )
    theme: List[AnyHttpUrl] = Field(
        description="A main category of the resource. A resource can have multiple themes.",
        rdf_term=DCAT.themeTaxonomy,
        rdf_type="uri"
    )
    title: List[LiteralField] = Field(
        description="A name given to the resource.",
        rdf_term=DCTERMS.title,
        rdf_type="rdfs_literal"
    )
    type: List[AnyHttpUrl] = Field(
        description="The nature or genre of the resource.",
        rdf_term=DCTERMS.type,
        rdf_type="uri")
    license: AnyHttpUrl = Field(
        description="A legal document under which the resource is made available.",
        rdf_term=DCTERMS.license,
        rdf_type="uri"
    )
    distribution: List[AnyHttpUrl] = Field(
        default=None,
        description="An available distribution of the dataset.",
        rdf_term=DCAT.distribution,
        rdf_type="uri"
    )
    project: List[AnyHttpUrl] = Field(
        default=None,
        description="connect dataset to the corresponding projects",
        rdf_term=FOAF.Project,
        rdf_type="uri"
    )
    has_version: List[AnyHttpUrl] = Field(
        default=None,
        description="This resource has a more specific, versioned resource",
        rdf_term=DCTERMS.hasVersion,
        rdf_type="uri"
    )
    in_series: List[AnyHttpUrl] = Field(
        default=None,
        description="A dataset series of which the dataset is part.",
        rdf_term=DCATv3.inSeries,
        rdf_type="uri"
    )

    @field_validator("title", "description", mode="before")
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
