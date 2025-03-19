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
from rdflib import DCAT, PROV, DCTERMS

from sempyro import RDFModel, LiteralField
from sempyro.hri_dcat import HRIDataset
from sempyro.namespaces import DISCO
from sempyro.utils.validator_functions import force_literal_field


class HRIStudy(RDFModel):
    model_config = ConfigDict(
                              json_schema_extra={
                                  "$ontology": ["https://rdf-vocabulary.ddialliance.org/discovery.html",
                                                "https://health-ri.atlassian.net/wiki/spaces/FSD/pages/121110529/Core+"
                                                "Metadata+Schema+Specification"],
                                  "$namespace": str(DISCO),
                                  "$IRI": DISCO.Study,
                                  "$prefix": "disco"
                              })

    dataset: List[Union[AnyHttpUrl, HRIDataset]] = Field(
        description="The dataset that was generated as a result of this study.",
        json_schema_extra={
            "rdf_term": PROV.generated,
            "rdf_type": "uri"
        }
    )
    title: List[LiteralField] = Field(
        description="The title of the study.",
        json_schema_extra={
            "rdf_term": DCTERMS.title,
            "rdf_type": "rdfs_literal"
        }
    )
    description: List[LiteralField] = Field(
        description="A free text description of the study.",
        json_schema_extra={
            "rdf_term": DCTERMS.description,
            "rdf_type": "literal"
        }
    )
    identifier: Union[str, LiteralField] = Field(
        description="A unique identifier of the study.",
        json_schema_extra={
            "rdf_term": DCTERMS.identifier,
            "rdf_type": "xsd:string"
        }
    )
    project: AnyHttpUrl = Field(
        description="The project of which this study is a part.",
        json_schema_extra={
            "rdf_term": DCTERMS.isPartOf,
            "rdf_type": "uri"
        }
    )

    @field_validator("title", "description", mode="before")
    @classmethod
    def convert_to_literal(cls, value: List[Union[str, LiteralField]]) -> List[LiteralField]:
        return [force_literal_field(item) for item in value]


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "hri_dcat")
    HRIStudy.save_schema_to_file(Path(json_models_folder, "HRIStudy.json"), "json")
    HRIStudy.save_schema_to_file(Path(json_models_folder, "HRIStudy.yaml"), "yaml")
