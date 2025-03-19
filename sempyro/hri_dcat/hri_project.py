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

from pydantic import AnyHttpUrl, ConfigDict, Field
from rdflib import DCAT, DCTERMS
from rdflib.namespace import FOAF

from sempyro.foaf import Project
from sempyro.hri_dcat.hri_catalog import HRICatalog


class HRIProject(Project):
    model_config = ConfigDict(
                              json_schema_extra={
                                  "$ontology": ["http://xmlns.com/foaf/spec/",
                                                "https://health-ri.atlassian.net/wiki/spaces/FSD/pages/121110529/Core+"
                                                "Metadata+Schema+Specification"],
                                  "$namespace": str(FOAF),
                                  "$IRI": FOAF.Project,
                                  "$prefix": "foaf"
                              })

    catalog: List[Union[AnyHttpUrl, HRICatalog]] = Field(
        description="A catalogue of which the project is part of.",
        json_schema_extra={
            "rdf_term": DCAT.resource,
            "rdf_type": "uri"
        }
    )

    study: List[AnyHttpUrl] = Field(
        default=None,
        description="A study that is performed in the context of the project.",
        json_schema_extra={
            "rdf_term": DCTERMS.hasPart,
            "rdf_type": "uri"
        }
    )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "hri_dcat")
    HRIProject.save_schema_to_file(Path(json_models_folder, "HRIProject.json"), "json")
    HRIProject.save_schema_to_file(Path(json_models_folder, "HRIProject.yaml"), "yaml")
