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

from pydantic import ConfigDict, AnyHttpUrl, Field

from sempyro import RDFModel
from sempyro.namespaces import DQV, OA


class QualityCertificate(RDFModel):
    model_config = ConfigDict(
        json_schema_extra={
            "$ontology": "https://www.w3.org/TR/vocab-dqv/",
            "$namespace": str(DQV),
            "$IRI": DQV.QualityCertificate,
            "$prefix": "dqv"
        }
    )

    target: AnyHttpUrl = Field(
        default=None,
        description="The relationship between an Annotation and its Target.",
        json_schema_extra={
            "rdf_term": OA.hasTarget,
            "rdf_type": "uri"
        }
    )
    body: AnyHttpUrl = Field(
        default=None,
        description="The object of the relationship is a resource that is a body of the Annotation.",
        json_schema_extra={
            "rdf_term": OA.hasBody,
            "rdf_type": "uri"
        }
    )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "dqv")
    QualityCertificate.save_schema_to_file(path=Path(json_models_folder, "QualityCertificate.json"), file_format="json")
    QualityCertificate.save_schema_to_file(path=Path(json_models_folder, "QualityCertificate.yaml"), file_format="yaml")
