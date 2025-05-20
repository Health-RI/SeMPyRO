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
from typing import List

from pydantic import ConfigDict, AnyHttpUrl, Field
from rdflib.namespace import DCAT, DCTERMS

from sempyro import RDFModel

class Relationship(RDFModel):
    model_config = ConfigDict(
        json_schema_extra={
            "$ontology": "https://www.w3.org/TR/vocab-dcat-3/",
            "$namespace": str(DCAT),
            "$IRI": DCAT.Relationship,
            "$prefix": "dcat"
        }
    )

    had_role: List[AnyHttpUrl] = Field(
        description="The function of an entity or agent with respect to another entity or resource.",
        json_schema_extra={
            "rdf_term": DCAT.hadRole,
            "rdf_type": "uri"
        }
    )
    relation: List[AnyHttpUrl] = Field(
        description="A related resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.relation,
            "rdf_type": "uri"
        }
    )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "dcat")
    Relationship.save_schema_to_file(path=Path(json_models_folder, "Relationship.json"), file_format="json")
    Relationship.save_schema_to_file(path=Path(json_models_folder, "Relationship.yaml"), file_format="yaml")
