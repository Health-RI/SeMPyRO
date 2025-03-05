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

import json
from pathlib import Path

import pytest

from sempyro.dcat import DCATDataService, DCATDatasetSeries, DCATCatalog, DCATDataset, DCATDistribution, DCATResource

MODELS_JSON_DIRECTORY = Path(Path(__file__).parents[1].resolve(), "models", "dcat")


@pytest.mark.parametrize("model_name", ["DCATResource",
                                        "DCATDataset",
                                        "DCATDatasetSeries",
                                        "DCATDataService",
                                        "DCATCatalog",
                                        "DCATDistribution"
                                        ])
def test_resource_models(model_name):
    with open(Path(MODELS_JSON_DIRECTORY, f"{model_name}.json")) as model_file:
        model_json = json.load(model_file)
    instance = globals()[model_name]
    actual_schema = instance.model_json_schema()
    assert json.dumps(model_json) == json.dumps(actual_schema)
