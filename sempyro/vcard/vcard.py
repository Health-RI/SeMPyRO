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
from pydantic import ConfigDict, Field, AnyHttpUrl, AnyUrl, field_validator
from pydantic.networks import validate_email
from rdflib import Namespace
import re
from typing import List, Union

from sempyro import RDFModel, LiteralField

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
                                  "$IRI": VCARD.VCard,
                                  "$prefix": "v"
                              }
                              )

    hasEmail: List[AnyUrl] = Field(default=None,
                                   description="The email address as a mailto URI",
                                   rdf_term=VCARD.hasEmail,
                                   rdf_type="uri"
                                   )
    full_name: List[Union[str, LiteralField]] = Field(default=None,
                                                      description="The full name of the object (as a single string). "
                                                                  "This is the only mandatory property.",
                                                      rdf_term=VCARD.fn,
                                                      rdf_type="rdfs_literal"
                                                      )
    hasUID: AnyHttpUrl = Field(description="A unique identifier for the object",
                               rdf_term=VCARD.hasUID,
                               rdf_type="uri"
                               )

    @classmethod
    def _convert_to_mailto(cls, value: str) -> AnyUrl:
        mail_part = value
        if value.startswith("mailto:"):
            mail_part = re.split(":|\//", value)[-1]
        mail_part = validate_email(mail_part)[1]
        return AnyUrl(f"mailto:{mail_part}")

    @field_validator("hasEmail", mode="before")
    @classmethod
    def _validate_email(cls, value: Union[str, AnyUrl]) -> List[AnyUrl]:
        """
        Checks if provided value is a valid email or mailto URI, fulfills an email to mailto URI
        """
        if not isinstance(value, list):
            value = [value]
        new_list = [cls._convert_to_mailto(item) for item in value]
        return new_list


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "vcard")
    VCard.save_schema_to_file(path=Path(json_models_folder, f"VCard.json"), file_format="json")
    VCard.save_schema_to_file(path=Path(json_models_folder, f"VCard.yaml"), file_format="yaml")
