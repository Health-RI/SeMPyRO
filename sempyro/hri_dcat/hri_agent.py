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

from pydantic import AnyUrl, ConfigDict, Field, field_validator
from rdflib.namespace import DCTERMS, FOAF

from sempyro import LiteralField
from sempyro.foaf import Agent
from sempyro.utils.validator_functions import validate_convert_email


class HRIAgent(Agent):
    model_config = ConfigDict(
        json_schema_extra={
            "$ontology": ["http://xmlns.com/foaf/spec/",
                          "https://health-ri.atlassian.net/wiki/spaces/FSD/pages/121110529/Core+"
                          "Metadata+Schema+Specification"],
            "$namespace": str(FOAF),
            "$IRI": FOAF.Agent,
            "$prefix": "foaf",
        }
    )

    name: Union[str, LiteralField] = Field(
        description="A name of the agent",
        json_schema_extra={
            "rdf_term": FOAF.name,
            "rdf_type": "rdfs_literal"
        }
    )
    identifier: Union[str, LiteralField] = Field(
        description="A unique identifier of the agent.",
        json_schema_extra={
            "rdf_term": DCTERMS.identifier,
            "rdf_type": "rdfs_literal"
        }
    )
    mbox: AnyUrl = Field(
        description="A personal mailbox, ie. an Internet mailbox associated "
        "with exactly one owner, the first owner of this mailbox.",
        json_schema_extra={
            "rdf_term": FOAF.mbox,
            "rdf_type": "uri",
        }
    )
    homepage: AnyUrl = Field(
        description="A webpage that either allows to make contact (i.e. a webform) or the information contains "
                    "how to get into contact.",
        json_schema_extra={
            "rdf_term": FOAF.homepage,
            "rdf_type": "uri",
        }
    )

    @field_validator("mbox", mode="before")
    @classmethod
    def _validate_email(cls, value: Union[str, AnyUrl, List[Union[str, AnyUrl]]]) -> List[AnyUrl]:
        """
        Checks if provided value is a valid email or mailto URI, fulfills an email to mailto URI
        """
        return validate_convert_email(value)


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "hri_dcat")
    HRIAgent.save_schema_to_file(path=Path(json_models_folder, "HRIAgent.json"), file_format="json")
    HRIAgent.save_schema_to_file(path=Path(json_models_folder, "HRIAgent.yaml"), file_format="yaml")
