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
from pydantic import ConfigDict, AnyHttpUrl, Field
from rdflib.namespace import DCAT
from typing import List, Union

from sempyro.dcat import DCATDataset, DCATResource


class DataService(DCATResource):
    """A collection of operations that provides access to one or more datasets or data processing functions."""
    model_config = ConfigDict(
                              json_schema_extra={
                                  "$ontology": "https://www.w3.org/TR/vocab-dcat-3/",
                                  "$namespace": str(DCAT),
                                  "$IRI": DCAT.DataService,
                                  "$prefix": "dcat"
                              }
                              )

    endpoint_description: List[Union[AnyHttpUrl, DCATResource]] = Field(
        default=None,
        description="A description of the services available via the end-points, including their operations, "
                    "parameters etc.",
        rdf_term=DCAT.endpointDescription,
        rdf_type="uri"
    )
    endpoint_url: List[Union[AnyHttpUrl, DCATResource]] = Field(
        description="The root location or primary endpoint of the service (a Web-resolvable IRI).",
        rdf_term=DCAT.endpointURL,
        rdf_type="uri"
    )
    serves_dataset: List[Union[AnyHttpUrl, DCATDataset]] = Field(
        default=None,
        description="A collection of data that this data service can distribute.",
        rdf_term=DCAT.servesDataset,
        rdf_type="uri"
    )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "dcat")
    DataService.save_schema_to_file(Path(json_models_folder, "DataService.json"), "json")
    DataService.save_schema_to_file(Path(json_models_folder, "DataService.yaml"), "yaml")
