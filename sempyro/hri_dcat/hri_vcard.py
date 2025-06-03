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

from pydantic import AnyHttpUrl, AnyUrl, ConfigDict, Field, field_validator
from rdflib import Namespace

from sempyro import LiteralField
from sempyro.utils.validator_functions import validate_convert_email
from sempyro.vcard import VCard

VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")


class HRIVCard(VCard):
    """
    The vCard class is equivalent to the new Kind class, which is the parent for the four explicit types
    of vCards (Individual, Organization, Location, Group)
    """
    model_config = ConfigDict(
                              json_schema_extra={
                                  "$ontology": ["https://www.w3.org/TR/vcard-rdf/",
                                                "https://health-ri.atlassian.net/wiki/spaces/FSD/pages/121110529/Core+"
                                                "Metadata+Schema+Specification"],
                                  "$namespace": str(VCARD),
                                  "$IRI": VCARD.Kind,
                                  "$prefix": "v"
                              }
                              )

    hasEmail: AnyUrl = Field(
        description="To specify the electronic mail address for communication with the object.",
        json_schema_extra={
            "rdf_term": VCARD.hasEmail,
            "rdf_type": "uri"
        })
    formatted_name: Union[str, LiteralField] = Field(
        description="The formatted text corresponding to the name of the object.",
        json_schema_extra={
            "rdf_term": VCARD.fn,
            "rdf_type": "rdfs_literal"
        })
    contact_page: List[AnyHttpUrl] = Field(
        default=None,
        description="A webpage that either allows to make contact (e.g. a webform) or provides information on how to get in touch.",
        json_schema_extra={
            "rdf_term": VCARD.hasURL,
            "rdf_type": "uri"
        }
    )

    @field_validator("hasEmail", mode="before")
    @classmethod
    def _validate_email(cls, value: Union[str, AnyUrl, List[Union[str, AnyUrl]]]) -> List[AnyUrl]:
        """
        Checks if provided value is a valid email or mailto URI, fulfills an email to mailto URI
        """
        return validate_convert_email(value)


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "hri_dcat")
    HRIVCard.save_schema_to_file(path=Path(json_models_folder, "HRIVCard.json"), file_format="json")
    HRIVCard.save_schema_to_file(path=Path(json_models_folder, "HRIVCard.yaml"), file_format="yaml")
