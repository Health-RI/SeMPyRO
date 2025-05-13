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

from pathlib import Path
from typing import List, Union

from pydantic import AnyHttpUrl, ConfigDict, Field, field_validator
from rdflib.namespace import DCAT, DCTERMS

from sempyro import LiteralField
from sempyro.dcat import DCATCatalog, DCATDataService, DCATDataset
from sempyro.hri_dcat.hri_data_service import HRIDataService
from sempyro.hri_dcat.hri_agent import HRIAgent
from sempyro.hri_dcat.hri_vcard import HRIVCard
from sempyro.namespaces import DCATAPv3
from sempyro.utils.validator_functions import force_literal_field


class HRICatalog(DCATCatalog):
    model_config = ConfigDict(
        json_schema_extra={
            "$ontology": ["https://www.w3.org/TR/vocab-dcat-3/",
                          "https://health-ri.atlassian.net/wiki/spaces/FSD/pages/121110529/Core+"
                          "Metadata+Schema+Specification"],
            "$namespace": str(DCAT),
            "$IRI": DCAT.Catalog,
            "$prefix": "dcat"
        }
    )
    title: List[LiteralField] = Field(
        description="A name given to the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.title,
            "rdf_type": "rdfs_literal"
        }
    )
    description: List[LiteralField] = Field(
        description="An account of the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.description,
            "rdf_type": "literal"
        }
    )
    publisher: Union[AnyHttpUrl, HRIAgent] = Field(
        description="An entity responsible for making the resource available.",
        json_schema_extra={
            "rdf_term": DCTERMS.publisher,
            "rdf_type": "uri"
        }
    )
    contact_point: Union[AnyHttpUrl, HRIVCard] = Field(
        description="Relevant contact information for the cataloged resource.",
        json_schema_extra={
            "rdf_term": DCAT.contactPoint,
            "rdf_type": "uri"
        }
    )
    dataset: List[Union[AnyHttpUrl, DCATDataset]] = Field(
        description="A dataset that is listed in the catalog.",
        json_schema_extra={
            "rdf_term": DCAT.dataset,
            "rdf_type": "uri"
        }
    )
    service: List[Union[AnyHttpUrl, HRIDataService]] = Field(
        default=None,
        description="A service that is listed in the catalog.",
        json_schema_extra={
            "rdf_term": DCAT.DataService,
            "rdf_type": "uri"
        }
    )
    catalog: List[Union[AnyHttpUrl, DCATCatalog]] = Field(
        default=None,
        description="A catalog that is listed in the catalog. HRI recommended",
        json_schema_extra={
            "rdf_term": DCAT.Catalog,
            "rdf_type": "uri"
        }
    )
    applicable_legislation: List[AnyHttpUrl] = Field(
        default=None,
        description="The legislation that is applicable to this resource.",
        json_schema_extra={
            "rdf_term": DCATAPv3.applicableLegislation,
            "rdf_type": "uri",
            # "bind_namespace": ['dcatap', DCATAPv3]
        }
    )
    modification_date: str = Field(
        default=None,
        description="Date of last update to the catalog.",
        json_schema_extra={
            "rdf_term": DCTERMS.modified,
            "rdf_type": "xsd:dateTime"
        }
    )
    release_date: str = Field(
        default=None,
        description="Date the catalog was first published.",
        json_schema_extra={
            "rdf_term": DCTERMS.issued,
            "rdf_type": "xsd:dateTime"
        }
    )


    @field_validator("title", "description", mode="before")
    @classmethod
    def convert_to_literal(cls, value: List[Union[str, LiteralField]]) -> List[LiteralField]:
        if not value:
            return None
        return [force_literal_field(item) for item in value]


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "hri_dcat")
    HRICatalog.save_schema_to_file(Path(json_models_folder, "HRICatalog.json"), "json")
    HRICatalog.save_schema_to_file(Path(json_models_folder, "HRICatalog.yaml"), "yaml")
