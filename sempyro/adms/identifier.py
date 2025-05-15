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

from pydantic import ConfigDict, Field
from rdflib.namespace import SKOS

from sempyro import LiteralField, RDFModel
from sempyro.namespaces import ADMS

class Identifier(RDFModel):
    model_config = ConfigDict(
        json_schema_extra={
            "$ontology": "http://www.w3.org/TR/vocab-adms/",
            "$namespace": str(ADMS),
            "$IRI": ADMS.Identifier,
            "$prefix": "adms"
        }
    )

    notation: Union[str, LiteralField] = Field(
        description="A string that is an identifier in the context of the identifier scheme referenced by its datatype.",
        json_schema_extra={
            "rdf_term": SKOS.notation,
            "rdf_type": "rdfs_literal"
        }
    )

    schema_agency: Union[str, LiteralField] = Field(
        default=None,
        description="The name of the agency that issued the identifier.",
        json_schema_extra={
            "rdf_term": ADMS.schemaAgency,
            "rdf_type": "rdfs_literal"
        }
    )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "adms")
    Identifier.save_schema_to_file(path=Path(json_models_folder, "Identifier.json"), file_format="json")
    Identifier.save_schema_to_file(path=Path(json_models_folder, "Identifier.yaml"), file_format="yaml")
