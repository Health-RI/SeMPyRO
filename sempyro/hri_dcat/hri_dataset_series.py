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

from pydantic import ConfigDict, Field, field_validator, AnyHttpUrl
from rdflib import DCAT, DCTERMS

from sempyro import LiteralField
from sempyro.dcat import DCATDatasetSeries
from sempyro.time import PeriodOfTime
from sempyro.vcard import VCard
from sempyro.namespaces import DCATv3, DCATAPv3
from sempyro.utils.validator_functions import force_literal_field


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
        default=None,
        description="Relevant contact information for the cataloged resource.",
        json_schema_extra={
            "rdf_term": DCAT.contactPoint,
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

    description: List[LiteralField] = Field(
        description="An account of the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.description,
            "rdf_type": "rdfs_literal"
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

    geographical_coverage: List[AnyHttpUrl] = Field(
        default=None,
        description="Spatial characteristics of the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.spatial,
            "rdf_type": "uri"
        }
    )

    temporal_coverage: List[Union[AnyHttpUrl, PeriodOfTime]] = Field(
        default=None,
        description="Temporal characteristics of the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.temporal,
            "rdf_type": "uri"
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
    HRIDatasetSeries.save_schema_to_file(Path(json_models_folder, "HRIDatasetSeries.json"), "json")
    HRIDatasetSeries.save_schema_to_file(Path(json_models_folder, "HRIDatasetSeries.yaml"), "yaml")
