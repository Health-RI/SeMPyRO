# Copyright 2025 Stichting Health-RI
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
from typing import Union

from pydantic import ConfigDict, AnyHttpUrl, Field
from rdflib.namespace import DCAT, PROV

from sempyro import RDFModel
from sempyro.foaf import Agent

class Attribution(RDFModel):
    model_config = ConfigDict(
        json_schema_extra={
            "$ontology": "https://www.w3.org/TR/prov-o/",
            "$namespace": str(PROV),
            "$IRI": PROV.Activity,
            "$prefix": "prov"
        }
    )

    agent: Union[AnyHttpUrl, Agent] = Field(
        default=None,
        description="The prov:agent property references an prov:Agent which influenced a resource.",
        json_schema_extra={
            "rdf_term": PROV.agent,
            "rdf_type": "uri"
        }
    )
    role: AnyHttpUrl = Field(
        default=None,
        description="The function of an entity or agent with respect to another entity or resource.",
        json_schema_extra={
            "rdf_term": DCAT.hadRole,
            "rdf_type": "uri"
        }
    )

if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "dcat")
    Attribution.save_schema_to_file(path=Path(json_models_folder, "Attribution.json"), file_format="json")
    Attribution.save_schema_to_file(path=Path(json_models_folder, "Attribution.yaml"), file_format="yaml")
