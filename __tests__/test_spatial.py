import json
from pathlib import Path
import pytest

from dcat.spatial import Location, Geometry


TEST_DATA_DIRECTORY = Path(Path(__file__).parent.resolve(), "test_data")
MODELS_JSON_DIRECTORY = Path(Path(__file__).parents[1].resolve(), "dcat", "json_models", "geo")


@pytest.mark.parametrize("model_name", ["Location", "Geometry"])
def test_vcard_agent(model_name):
    with open(Path(MODELS_JSON_DIRECTORY, f"{model_name}.json"), "r") as model_file:
        model_json = json.load(model_file)
    instance = globals()[model_name]
    actual_schema = instance.model_json_schema()
    assert json.dumps(model_json) == json.dumps(actual_schema)