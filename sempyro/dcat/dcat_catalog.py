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
from rdflib.namespace import DCAT, FOAF

from sempyro.dcat import DCATDataset
from sempyro.dcat.dcat_catalog_record import DCATCatalogRecord


class DCATCatalog(DCATDataset):
    """A curated collection of metadata about resources."""
    model_config = ConfigDict(json_schema_extra={
                                  "$ontology": "https://www.w3.org/TR/vocab-dcat-3/",
                                  "$namespace": str(DCAT),
                                  "$IRI": DCAT.Catalog,
                                  "$prefix": "dcat"
                              })

    catalog_record: List[Union[AnyHttpUrl, DCATCatalogRecord]] = Field(
        default=None,
        description="A record describing the registration of a single resource (e.g., a dataset, a data service) that "
                     "is part of the catalog.",
        json_schema_extra={
            "rdf_term": DCAT.record,
            "rdf_type": "uri"
        }
    )
    dataset: List[Union[AnyHttpUrl, DCATDataset]] = Field(
        default=None,
        description="A dataset that is listed in the catalog.",
        json_schema_extra={
            "rdf_term": DCAT.dataset,
            "rdf_type": "uri"
        }
    )
    service: List[AnyHttpUrl] = Field(
        default=None,
        description="A service that is listed in the catalog.",
        json_schema_extra={
            "rdf_term": DCAT.service,
            "rdf_type": "uri"
        }
    )
    catalog: List[AnyHttpUrl] = Field(
        default=None,
        description="A catalog that is listed in the catalog.",
        json_schema_extra={
            "rdf_term": DCAT.catalog,
            "rdf_type": "uri"
        }
    )
    homepage: AnyHttpUrl = Field(
        default=None,
        description="A homepage of the catalog (a public Web document usually available in HTML).",
        json_schema_extra={
            "rdf_term": FOAF.homepage,
            "rdf_type": "uri"
        }
    )
    themes: List[AnyHttpUrl] = Field(
        default=None,
        description="A knowledge organization system (KOS) used to classify the resources documented in the catalog "
                    "(e.g., datasets and services).",
        json_schema_extra={
            "rdf_term": DCAT.themeTaxonomy,
            "rdf_type": "uri"
        }
    )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "dcat")
    DCATCatalog.save_schema_to_file(Path(json_models_folder, "DCATCatalog.json"), "json")
    DCATCatalog.save_schema_to_file(Path(json_models_folder, "DCATCatalog.yaml"), "yaml")
