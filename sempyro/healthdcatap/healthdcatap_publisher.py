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

from pydantic import ConfigDict, Field
from rdflib.namespace import DCAT, DCTERMS, FOAF

from sempyro import LiteralField
from sempyro.healthdcatap.healthdcatap_agent import HEALTHDCATAPAgent
from sempyro.healthdcatap.healthdcatap_kind import HEALTHDCATAPKind


class HEALTHDCATAPPublisher(HEALTHDCATAPAgent):
    """
    Agent responsible for making the health data resource available.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "$ontology": [
                "https://xmlns.com/foaf/spec/",
                "https://healthdataeu.pages.code.europa.eu/healthdcat-ap/releases/release-6/",
            ],
            "$namespace": str(FOAF),
            "$IRI": FOAF.Agent,
            "$prefix": "foaf",
        }
    )
    contact_point: HEALTHDCATAPKind = Field(
        description="Contact information that can be used to contact the Agent.",
        json_schema_extra={
            "rdf_term": DCAT.contactPoint,
            "rdf_type": "uri",
        },
    )
    description: List[Union[str, LiteralField]] = Field(
        default=None,
        description="A description of the publisher activities.",
        json_schema_extra={
            "rdf_term": DCTERMS.description,
            "rdf_type": "rdfs_literal",
        },
    )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "health_dcat")
    HEALTHDCATAPPublisher.save_schema_to_file(Path(json_models_folder, "HEALTHDCATAPPublisher.json"), "json")
    HEALTHDCATAPPublisher.save_schema_to_file(Path(json_models_folder, "HEALTHDCATAPPublisher.yaml"), "yaml")
