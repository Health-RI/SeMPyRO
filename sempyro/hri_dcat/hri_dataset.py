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
from typing import List, Union

from pydantic import AnyHttpUrl, AwareDatetime, ConfigDict, Field, NaiveDatetime, field_validator
from rdflib.namespace import DCAT, DCTERMS, FOAF

from sempyro import LiteralField
from sempyro.dcat import DCATDataset, AccessRights
from sempyro.hri_dcat.hri_agent import HRIAgent
from sempyro.hri_dcat.hri_vcard import HRIVCard
from sempyro.hri_dcat.vocabularies import DatasetTheme
from sempyro.namespaces import DCATv3, DCATAPv3
from sempyro.utils.validator_functions import date_handler, force_literal_field


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

    access_rights: AccessRights = Field(
        description="Information about who can access the resource or an indication of its security status.",
        json_schema_extra={
            "rdf_term": DCTERMS.accessRights,
            "rdf_type": "uri"
        }
    )

    applicable_legislation: List[AnyHttpUrl] = Field(
        description="The legislation that is applicable to this resource.",
        json_schema_extra={
            "rdf_term": DCATAPv3.applicableLegislation,
            "rdf_type": "uri",
            "bind_namespace": ['dcatap', DCATAPv3]
        }
    )

    contact_point: Union[AnyHttpUrl, HRIVCard] = Field(
        description="Relevant contact information for the cataloged resource.",
        json_schema_extra={
            "rdf_term": DCAT.contactPoint,
            "rdf_type": "uri"
        }
    )
    creator: List[Union[AnyHttpUrl, HRIAgent]] = Field(
        description="The entity responsible for producing the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.creator,
            "rdf_type": "uri"
        }
    )
    description: List[LiteralField] = Field(
        description="An account of the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.description,
            "rdf_type": "literal"
        }
    )
    issued: Union[str, datetime, date, AwareDatetime, NaiveDatetime] = Field(
        default=None,
        description="Date of formal issuance of the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.issued,
            "rdf_type": "datetime_literal"
        }
    )
    identifier: Union[str, LiteralField] = Field(
        description="An unambiguous reference to the resource within a given context.",
        json_schema_extra={
            "rdf_term": DCTERMS.identifier,
            "rdf_type": "rdfs_literal"
        }
    )
    modified: Union[str, date, AwareDatetime, NaiveDatetime] = Field(
        default=None,
        description="Date on which the resource was changed.",
        json_schema_extra={
            "rdf_term": DCTERMS.modified,
            "rdf_type": "datetime_literal"
        }
    )
    publisher: Union[AnyHttpUrl, HRIAgent] = Field(
        description="An entity responsible for making the resource available.",
        json_schema_extra={
            "rdf_term": DCTERMS.publisher,
            "rdf_type": "uri"
        }
    )
    theme: List[DatasetTheme] = Field(
        description="A main category of the resource. A resource can have multiple themes.",
        json_schema_extra={
            "rdf_term": DCAT.theme,
            "rdf_type": "uri"
        }
    )
    title: List[LiteralField] = Field(
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
    distribution: List[AnyHttpUrl] = Field(
        default=None,
        description="The nature or genre of the resource.",
        json_schema_extra={
            "rdf_term": DCAT.distribution,
            "rdf_type": "uri"
        }
    )
    version: List[LiteralField] = Field(
        default=None,
        description="The version indicator (name or identifier) of a resource.",
        json_schema_extra={
            "rdf_term": DCATv3.version,
            "rdf_type": "rdfs_literal"
        }
    )
    in_series: List[AnyHttpUrl] = Field(
        default=None,
        description="A dataset series of which the dataset is part.",
        json_schema_extra={
            "rdf_term": DCATv3.inSeries,
            "rdf_type": "uri"
        }
    )
    keyword: List[LiteralField] = Field(
        description="A keyword or tag describing the resource.",
        json_schema_extra={
            "rdf_term": DCAT.keyword,
            "rdf_type": "rdfs_literal"
        }
    )

    @field_validator("title", "description", "keyword", mode="before")
    @classmethod
    def convert_to_literal(cls, value: Union[List[Union[str, LiteralField]], None]) -> Union[List[LiteralField], None]:
        if not value:
            return None
        return [force_literal_field(item) for item in value]

    @field_validator("issued", mode="before")
    @classmethod
    def date_validator(cls, value):
        return date_handler(value)


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "hri_dcat")
    HRIDataset.save_schema_to_file(Path(json_models_folder, "HRIDataset.json"), "json")
    HRIDataset.save_schema_to_file(Path(json_models_folder, "HRIDataset.yaml"), "yaml")
