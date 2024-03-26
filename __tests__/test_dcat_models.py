import json
from pathlib import Path
import pytest

from sempyro.dcat.dcat_resource import DCATResource
from sempyro.dcat.dcat_dataset import DCATDataset
from sempyro.dcat.dataset_series import DatasetSeries
from sempyro.dcat.data_service import DataService
from sempyro.dcat.dcat_catalog import DCATCatalog
from sempyro.dcat.dcat_distribution import DCATDistribution


MODELS_JSON_DIRECTORY = Path(Path(__file__).parents[1].resolve(), "sempyro", "dcat", "json_models")


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
