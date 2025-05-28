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

from pydantic import ConfigDict, Field, AnyHttpUrl

from rdflib import DCAT, DCTERMS

from sempyro.dcat import DCATDatasetSeries
from sempyro.foaf import Agent
from sempyro.vcard import VCard
from sempyro.namespaces import DCATv3, DCATAPv3


class HRIDatasetSeries(DCATDatasetSeries):
    model_config = ConfigDict(
        json_schema_extra={
            "$ontology": ["https://www.w3.org/TR/vocab-dcat-3/",
                          "https://health-ri.atlassian.net/wiki/spaces/FSD/pages/121110529/Core+"
                          "Metadata+Schema+Specification"],
            "$namespace": str(DCAT),
            "$IRI": DCATv3.DatasetSeries,
            "$prefix": "dcat"
        }
    )

    applicable_legislation: List[AnyHttpUrl] = Field(
        default=None,
        description="The legislation that is applicable to this resource.",
        json_schema_extra={
            "rdf_term": DCATAPv3.applicableLegislation,
            "rdf_type": "uri"
        }
    )
    contact_point: List[Union[AnyHttpUrl, VCard]] = Field(
        description="Relevant contact information for the cataloged resource.",
        json_schema_extra={
            "rdf_term": DCAT.contactPoint,
            "rdf_type": "uri"
        }
    )
    frequency: AnyHttpUrl = Field(
        default=None,
        description="The frequency with which items are added to a collection.",
        json_schema_extra={
            "rdf_term": DCTERMS.accrualPeriodicity,
            "rdf_type": "uri"
        }
    )
    publisher: Union[AnyHttpUrl, Agent] = Field(
        default=None,
        description="The entity responsible for making the resource available.",
        json_schema_extra={
            "rdf_term": DCTERMS.publisher,
            "rdf_type": "uri"
        }
    )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "hri_dcat")
    HRIDatasetSeries.save_schema_to_file(Path(json_models_folder, "HRIDatasetSeries.json"), "json")
    HRIDatasetSeries.save_schema_to_file(Path(json_models_folder, "HRIDatasetSeries.yaml"), "yaml")
