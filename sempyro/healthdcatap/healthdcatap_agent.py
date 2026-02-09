# Copyright 2026 Stichting Health-RI
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
from pydantic import AnyHttpUrl, ConfigDict, Field
from rdflib.namespace import DCTERMS, FOAF

from sempyro.foaf import Agent


class HEALTHDCATAPAgent(Agent):
    model_config = ConfigDict(
        json_schema_extra={
            "$ontology": [
                "https://xmlns.com/foaf/spec/",
                "https://healthdataeu.pages.code.europa.eu/healthdcat-ap/releases/release-6/",
            ],
            "$namespace": str(FOAF),
            "$IRI": FOAF.Agent,
            "$prefix": "foaf",
        },
    )
    type: AnyHttpUrl = Field(
        default=None,
        description="The nature of the agent.",
        json_schema_extra={
            "rdf_term": DCTERMS.type,
            "rdf_type": "uri",
        },
    )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "health_dcat")
    HEALTHDCATAPAgent.save_schema_to_file(path=Path(json_models_folder, "HEALTHDCATAPAgent.json"), file_format="json")
    HEALTHDCATAPAgent.save_schema_to_file(path=Path(json_models_folder, "HEALTHDCATAPAgent.yaml"), file_format="yaml")
