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

import re
from pathlib import Path
from typing import List, Union

from pydantic import AnyHttpUrl, AnyUrl, ConfigDict, Field, field_validator
from pydantic.networks import validate_email
from rdflib import Namespace

from sempyro import LiteralField, RDFModel
from sempyro.utils.validator_functions import validate_convert_email

VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")


class VCard(RDFModel):
    """
    The vCard class is equivalent to the new Kind class, which is the parent for the four explicit types
    of vCards (Individual, Organization, Location, Group)
    """
    model_config = ConfigDict(
                              json_schema_extra={
                                  "$ontology": "https://www.w3.org/TR/vcard-rdf/",
                                  "$namespace": str(VCARD),
                                  "$IRI": VCARD.Kind,
                                  "$prefix": "v"
                              }
                              )

    hasEmail: List[AnyUrl] = Field(default=None,
                                   description="The email address as a mailto URI",
                                   json_schema_extra={
                                       "rdf_term": VCARD.hasEmail,
                                       "rdf_type": "uri"
                                   }
                                   )
    formatted_name: List[Union[str, LiteralField]] = Field(
        default=None,
        description="The full name of the object (as a single string). " 
                    "This is the only mandatory property.",
        json_schema_extra={
            "rdf_term": VCARD.fn,
            "rdf_type": "rdfs_literal"
        }
    )
    hasUID: AnyHttpUrl = Field(
        default=None,
        description="A unique identifier for the object", 
        json_schema_extra={ 
            "rdf_term": VCARD.hasUID, 
            "rdf_type": "uri" 
        }
    )

    @field_validator("hasEmail", mode="before")
    @classmethod
    def _validate_email(cls, value: Union[str, AnyUrl, List[Union[str, AnyUrl]]]) -> List[AnyUrl]:
        """
        Checks if provided value is a valid email or mailto URI, fulfills an email to mailto URI
        """
        if not isinstance(value, list):
            value = [value]
        return validate_convert_email(value)


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "vcard")
    VCard.save_schema_to_file(path=Path(json_models_folder, "VCard.json"), file_format="json")
    VCard.save_schema_to_file(path=Path(json_models_folder, "VCard.yaml"), file_format="yaml")
