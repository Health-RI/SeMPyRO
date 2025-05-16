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

from pydantic import AnyUrl, AnyHttpUrl, ConfigDict, Field, field_validator
from rdflib import URIRef
from rdflib.namespace import DCTERMS, FOAF

from sempyro import LiteralField
from sempyro.foaf import Agent
from sempyro.geo import Location
from sempyro.namespaces import HEALTHDCATAP
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

    name: List[Union[str, LiteralField]] = Field(
        description="A name for some thing.",
        json_schema_extra={
            "rdf_term": FOAF.name,
            "rdf_type": "rdfs_literal"
        }
    )
    identifier: List[Union[str, LiteralField]] = Field(
        description="An unambiguous reference to the resource within a given context.",
        json_schema_extra={
            "rdf_term": DCTERMS.identifier,
            "rdf_type": "rdfs_literal"
        }
    )
    mbox: AnyUrl = Field(
        description="A email address via which contact can be made. " 
                    "This property SHOULD be used to provide the email address of the Agent, " 
                    "specified using fully qualified mailto: URI scheme [RFC6068]." 
                    "The email SHOULD be used to establish a communication channel to the agent.",
        json_schema_extra={
            "rdf_term": FOAF.mbox,
            "rdf_type": "uri",
        }
    )
    homepage: AnyUrl = Field(
        description="A homepage for some thing.",
        json_schema_extra={
            "rdf_term": FOAF.homepage,
            "rdf_type": "uri",
        }
    )
    spatial: List[Union[AnyHttpUrl, Location]] = Field(
        default=None,
        description="Spatial characteristics of the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.spatial,
            "rdf_type": "uri"
        }
    )
    publisher_note: Union[str, LiteralField] = Field(
        default=None,
        description="A description of the publisher activities.",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.publisherNote,
            "rdf_type": "rdfs_literal"
        }
    )
    publisher_type: Union[AnyUrl, URIRef] = Field(
        default=None,
        description="A type of organisation that makes the Dataset available.",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.publisherType,
            "rdf_type": "uri"
        }
    )
    type: AnyHttpUrl = Field(
        default=None,
        description="The nature or genre of the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.type,
            "rdf_type": "uri"
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
