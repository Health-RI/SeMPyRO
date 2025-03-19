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

from pydantic import ConfigDict, Field, field_validator
from rdflib import DCAT, DCTERMS

from sempyro import LiteralField
from sempyro.dcat import DCATDatasetSeries
from sempyro.namespaces import DCATv3
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

    title: List[LiteralField] = Field(
        description="A name given to the Dataset Series. HRI mandatory",
        json_schema_extra={
            "rdf_term": DCTERMS.title,
            "rdf_type": "rdfs_literal"
        }
    )

    description: List[LiteralField] = Field(
        description="A free-text account of the Dataset Series. HRI mandatory",
        json_schema_extra={
            "rdf_term": DCTERMS.description,
            "rdf_type": "rdfs_literal"
        }
    )

    @field_validator("title", "description", mode="before")
    @classmethod
    def convert_to_literal(cls, value: List[Union[str, LiteralField]]) -> List[LiteralField]:
        return [force_literal_field(item) for item in value]

if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "hri_dcat")
    HRIDatasetSeries.save_schema_to_file(Path(json_models_folder, "HRIDatasetSeries.json"), "json")
    HRIDatasetSeries.save_schema_to_file(Path(json_models_folder, "HRIDatasetSeries.yaml"), "yaml")
