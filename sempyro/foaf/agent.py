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

from sempyro import RDFModel, LiteralField
from pydantic import ConfigDict, Field
from rdflib.namespace import DCTERMS, FOAF


class Agent(RDFModel):
    model_config = ConfigDict(
                              json_schema_extra={
                                  "$ontology": "http://xmlns.com/foaf/spec/",
                                  "$namespace": str(FOAF),
                                  "$IRI": FOAF.Agent,
                                  "$prefix": "foaf"
                              }
                              )

    name: List[Union[str, LiteralField]] = Field(description="A name of the agent",
                                                 rdf_term=FOAF.name,
                                                 rdf_type="rdfs_literal"
                                                 )
    identifier: Union[str, LiteralField] = Field(description="A unique identifier of the agent.",
                                                 rdf_term=DCTERMS.identifier,
                                                 rdf_type="rdfs_literal")


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "foaf")
    Agent.save_schema_to_file(path=Path(json_models_folder, f"Agent.json"), file_format="json")
    Agent.save_schema_to_file(path=Path(json_models_folder, f"Agent.yaml"), file_format="yaml")
