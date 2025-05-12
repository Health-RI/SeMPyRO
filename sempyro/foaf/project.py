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
from rdflib.namespace import DCTERMS, FOAF

from sempyro import LiteralField, RDFModel
from sempyro.foaf import Agent
from sempyro.utils.validator_functions import force_literal_field


class Project(RDFModel):
    model_config = ConfigDict(
                              json_schema_extra={
                                  "$ontology": ["http://xmlns.com/foaf/spec/",
                                                "https://health-ri.atlassian.net/wiki/spaces/FSD/pages/121110529/Core+"
                                                "Metadata+Schema+Specification"],
                                  "$namespace": str(FOAF),
                                  "$IRI": FOAF.Project,
                                  "$prefix": "foaf"
                              }
                              )
    description: List[LiteralField] = Field(
        description="A free-text description of the project.",
        json_schema_extra={
            "rdf_term": DCTERMS.description,
            "rdf_type": "literal"
        }
    )
    identifier: Union[str, LiteralField] = Field(
        description="A unique identifier of the resource being described or cataloged.",
        json_schema_extra={
            "rdf_term": DCTERMS.identifier,
            "rdf_type": "xsd:string"
        }
    )
    title: List[LiteralField] = Field(
        description="A name given to the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.title,
            "rdf_type": "rdfs_literal"
        }
    )
    funded_by: List[Union[AnyHttpUrl, Agent]] = Field(
        description="An organization funding a project or person.",
        json_schema_extra={
            "rdf_term": FOAF.fundedBy,
            "rdf_type": "uri"
        },
        alias="funder"
    )
    relation: List[AnyHttpUrl] = Field(
        default=None,
        description="Link to the project datasets",
        json_schema_extra={
            "rdf_term": DCTERMS.relation,
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
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "foaf")
    Project.save_schema_to_file(Path(json_models_folder, "Project.json"), "json")
    Project.save_schema_to_file(Path(json_models_folder, "Project.yaml"), "yaml")
