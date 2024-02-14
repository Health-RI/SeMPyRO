import json
from pathlib import Path
import pytest

from dcat.policy import ODRLPolicy


TEST_DATA_DIRECTORY = Path(Path(__file__).parent.resolve(), "test_data")
MODELS_JSON_DIRECTORY = Path(Path(__file__).parents[1].resolve(), "dcat", "json_models")


def test_vcard_agent():
    with open(Path(MODELS_JSON_DIRECTORY, f"ODRLPolicy.json"), "r") as model_file:
        model_json = json.load(model_file)
    actual_schema = ODRLPolicy.model_json_schema()
    assert json.dumps(model_json) == json.dumps(actual_schema)
