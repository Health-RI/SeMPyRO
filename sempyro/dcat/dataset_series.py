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

from pydantic import ConfigDict
from rdflib import DCAT

from sempyro.dcat import DCATResource
from sempyro.namespaces import DCATv3


class DCATDatasetSeries(DCATResource):
    """A collection of datasets that are published separately, but share some characteristics that group them"""
    model_config = ConfigDict(title=DCATv3.DatasetSeries,
                              json_schema_extra={
                                  "$ontology": "https://www.w3.org/TR/vocab-dcat-3/",
                                  "$namespace": str(DCAT),
                                  "$IRI": DCATv3.DatasetSeries,
                                  "$prefix": "dcat"
                              }
                              )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "dcat")
    DCATDatasetSeries.save_schema_to_file(Path(json_models_folder, "DCATDatasetSeries.json"), "json")
    DCATDatasetSeries.save_schema_to_file(Path(json_models_folder, "DCATDatasetSeries.yaml"), "yaml")
