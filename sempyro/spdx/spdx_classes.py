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
from typing import Union

from pydantic import AnyHttpUrl, ConfigDict, Field
from rdflib import Namespace

from sempyro import LiteralField, RDFModel

SPDX = Namespace("http://spdx.org/rdf/terms#")


class Checksum(RDFModel):
    """
    A Checksum is value that allows the contents of a file to be authenticated. 
    Even small changes to the content of the file will change its checksum. 
    This class allows the results of a variety of checksum and cryptographic message digest algorithms to be 
    represented.
    """
    model_config = ConfigDict(json_schema_extra={
                                  "$ontology": "http://spdx.org/rdf/terms/2.3",
                                  "$namespace": str(SPDX),
                                  "$IRI": SPDX.Checksum,
                                  "$prefix": "spdx"
                              }
                              )

    algorithm: AnyHttpUrl = Field(
        description="The algorithm used to produce the subject Checksum.",
        json_schema_extra={
            "rdf_term": SPDX.algorithm,
            "rdf_type": "uri"
        }
    )
    checksum_value: Union[str, LiteralField] = Field(
        description="A lower case hexadecimal encoded digest value produced using a specific algorithm.",
        json_schema_extra={
            "rdf_term": SPDX.checksumValue,
            "rdf_type": "xsd:hexBinary"
        }
    )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "spdx")
    Checksum.save_schema_to_file(Path(json_models_folder, "Checksum.json"), "json")
    Checksum.save_schema_to_file(Path(json_models_folder, "Checksum.yaml"), "yaml")

