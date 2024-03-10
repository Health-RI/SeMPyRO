import json
from pathlib import Path
import pytest

from hri_dcat.hri_dataset import HRIDataset
from hri_dcat.project import Project
from hri_dcat.hri_data_service import HRIDataService
from hri_dcat.hri_catalog import HRICatalog
from hri_dcat.hri_distribution import HRIDistribution

MODELS_JSON_DIRECTORY = Path(Path(__file__).parents[1].resolve(), "hri_dcat", "json_models")


@pytest.mark.parametrize("model_name", ["Project",
                                        "HRIDataset",
                                        "HRIDataService",
                                        "HRICatalog",
                                        "HRIDistribution"
                                        ])
def test_hri_models(model_name):
    with open(Path(MODELS_JSON_DIRECTORY, f"{model_name}.json"), "r") as model_file:
        model_json = json.load(model_file)
    instance = globals()[model_name]
    actual_schema = instance.model_json_schema()
    assert json.dumps(model_json) == json.dumps(actual_schema)