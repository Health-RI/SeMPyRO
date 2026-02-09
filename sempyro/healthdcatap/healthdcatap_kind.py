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
from typing import List, Union

from pydantic import AnyHttpUrl, AnyUrl, ConfigDict, Field, field_validator
from rdflib import Namespace

from sempyro import LiteralField
from sempyro.utils.validator_functions import validate_convert_email
from sempyro.vcard import VCard

VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")


class HEALTHDCATAPKind(VCard):
    """
    A description following the vCard specification.
    The Kind class is the parent class for Individual, Organization, Location, Group.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "$ontology": [
                "https://www.w3.org/TR/vcard-rdf/",
                "https://healthdataeu.pages.code.europa.eu/healthdcat-ap/releases/release-6/",
            ],
            "$namespace": str(VCARD),
            "$IRI": VCARD.Kind,
            "$prefix": "v",
        },
    )
    hasEmail: AnyUrl = Field(
        default=None,
        description="A email address via which contact can be made.",
        json_schema_extra={
            "rdf_term": VCARD.hasEmail,
            "rdf_type": "uri",
        },
    )
    contact_page: AnyHttpUrl = Field(
        default=None,
        description="A webpage that either allows to make contact or provides information on how to get in touch.",
        json_schema_extra={
            "rdf_term": VCARD.hasURL,
            "rdf_type": "uri",
        },
    )
    @field_validator("hasEmail", mode="before")
    @classmethod
    def _validate_email(cls, value: Union[str, AnyUrl, List[Union[str, AnyUrl]]]) -> AnyUrl:
        """
        Checks if provided value is a valid email or mailto URI, fulfills an email to mailto URI
        """
        converted = validate_convert_email(value)
        if isinstance(converted, list):
            return converted[0]
        return converted


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "health_dcat")
    HEALTHDCATAPKind.save_schema_to_file(Path(json_models_folder, "HEALTHDCATAPKind.json"), "json")
    HEALTHDCATAPKind.save_schema_to_file(Path(json_models_folder, "HEALTHDCATAPKind.yaml"), "yaml")
