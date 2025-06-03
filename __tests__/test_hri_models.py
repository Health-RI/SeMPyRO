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

from sempyro.foaf import Project
from sempyro.hri_dcat import (
    HRICatalog,
    HRIDataService,
    HRIDataset,
    HRIDistribution,
    HRIDatasetSeries,
    HRIAgent
)

MODELS_JSON_DIRECTORY = Path(Path(__file__).parents[1].resolve(), "models")


@pytest.mark.parametrize("model_name", [
                                        "HRIDataset",
                                        "HRIDataService",
                                        "HRICatalog",
                                        "HRIDistribution",
                                        "HRIDatasetSeries",
                                        "HRIAgent"
                                        ])
def test_hri_models(model_name):
    with open(Path(MODELS_JSON_DIRECTORY, "hri_dcat", f"{model_name}.json")) as model_file:
        model_json = json.load(model_file)
    instance = globals()[model_name]
    actual_schema = instance.model_json_schema()
    assert json.dumps(model_json) == json.dumps(actual_schema)


def test_project():
    with open(Path(MODELS_JSON_DIRECTORY, "foaf", "Project.json")) as model_file:
        model_json = json.load(model_file)
    actual_schema = Project.model_json_schema()
    assert json.dumps(model_json) == json.dumps(actual_schema)
