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

from sempyro.dcat import DCATResource
from sempyro.dcat import DCATDataset
from sempyro.dcat.dataset_series import DatasetSeries
from sempyro.dcat.data_service import DataService
from sempyro.dcat.dcat_catalog import DCATCatalog
from sempyro.dcat.dcat_distribution import DCATDistribution


MODELS_JSON_DIRECTORY = Path(Path(__file__).parents[1].resolve(), "models", "dcat")


@pytest.mark.parametrize("model_name", ["DCATResource",
                                        "DCATDataset",
                                        "DatasetSeries",
                                        "DataService",
                                        "DCATCatalog",
                                        "DCATDistribution"
                                        ])
def test_resource_models(model_name):
    with open(Path(MODELS_JSON_DIRECTORY, f"{model_name}.json"), "r") as model_file:
        model_json = json.load(model_file)
    instance = globals()[model_name]
    actual_schema = instance.model_json_schema()
    assert json.dumps(model_json) == json.dumps(actual_schema)
