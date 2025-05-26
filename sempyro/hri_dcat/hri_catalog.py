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

from pydantic import AnyHttpUrl, ConfigDict, Field
from rdflib.namespace import DCAT, DCTERMS

from sempyro.dcat import DCATCatalog, DCATDataset
from sempyro.hri_dcat.hri_data_service import HRIDataService
from sempyro.hri_dcat.hri_agent import HRIAgent
from sempyro.hri_dcat.hri_vcard import HRIVCard
from sempyro.namespaces import DCATAPv3


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
    publisher: Union[AnyHttpUrl, HRIAgent] = Field(
        description="An entity responsible for making the resource available.",
        json_schema_extra={
            "rdf_term": DCTERMS.publisher,
            "rdf_type": "uri"
        }
    )
    creator: List[Union[AnyHttpUrl, HRIAgent]] = Field(
        default=None,
        description="The entity responsible for producing the resource. Resources of type foaf:Agent are "
                    "recommended as values for this property.",
        json_schema_extra={
            "rdf_term": DCTERMS.creator,
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
            "rdf_term": DCAT.service,
            "rdf_type": "uri"
        }
    )
    catalog: List[AnyHttpUrl] = Field(
        default=None,
        description="A catalog that is listed in the catalog. HRI recommended",
        json_schema_extra={
            "rdf_term": DCAT.catalog,
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
    has_part: List[Union[AnyHttpUrl, DCATCatalog]] = Field(
        default=None,
        description="A related resource that is included either physically or logically in the described resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.hasPart,
            "rdf_type": "uri"
        }
    )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "hri_dcat")
    HRICatalog.save_schema_to_file(Path(json_models_folder, "HRICatalog.json"), "json")
    HRICatalog.save_schema_to_file(Path(json_models_folder, "HRICatalog.yaml"), "yaml")
