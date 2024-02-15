import json
from pathlib import Path
import pytest

from dcat.dcat_resource import DCATResource
from dcat.dcat_dataset import DCATDataset
from dcat.dataset_series import DatasetSeries
from dcat.data_service import DatasetService

TEST_DATA_DIRECTORY = Path(Path(__file__).parent.resolve(), "test_data")
MODELS_JSON_DIRECTORY = Path(Path(__file__).parents[1].resolve(), "dcat", "json_models")


@pytest.mark.parametrize("model_name", ["DCATResource",
                                        "DCATDataset",
                                        "DatasetSeries",
                                        "DatasetService"])
def test_resource_models(model_name):
    with open(Path(MODELS_JSON_DIRECTORY, f"{model_name}.json"), "r") as model_file:
        model_json = json.load(model_file)
    instance = globals()[model_name]
    actual_schema = instance.model_json_schema()
    assert json.dumps(model_json) == json.dumps(actual_schema)
