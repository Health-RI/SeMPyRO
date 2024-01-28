import json

import pytest

from pathlib import Path
from pydantic_core import ValidationError
from dcat.dcat_time_models import TimePosition
from rdflib import Graph, DCAT, Namespace, RDF, DCTERMS

TEST_DATA_DIRECTORY = Path(Path(__file__).parent.resolve(), "test_data")

EX = Namespace("http://example.com")


@pytest.mark.parametrize("input_file", ["time_position_nominal.json", "time_position_numeric.json"])
def test_time_position(input_file):
    with open(Path(TEST_DATA_DIRECTORY, input_file), "r") as file:
        assert TimePosition.model_validate_json(file.read())


@pytest.mark.parametrize("data", [
    {"hasTRS": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"},
    {"hasTRS": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian",
     "numericPosition": 541.0,
     "nominalPosition": "Trias"},
    {"numericPosition": 541.0}
                                  ])
def test_time_position_validation(data):
    with pytest.raises(ValidationError):
        TimePosition(**data)


# def test_time_position_to_graph():
#     time_position_start = TimePosition(hasTRS="http://resource.geosciml.org/classifier/cgi/geologicage/ma",
#                                        numericPosition=541.0)
#     time_position_end = TimePosition(hasTRS="http://resource.geosciml.org/classifier/cgi/geologicage/ma",
#                                      numericPosition=251.902)
#     graph = Graph()
#     subject = EX.ds850
#     graph.bind("ex", EX)
#     graph.add((subject, RDF.type, DCAT.Dataset))
#     graph.add((subject, DCTERMS.temporal, DCTERMS.PeriodOfTime))
#     graph.add((DCTERMS.PeriodOfTime, ))
#     time_position_start.to_graph_node(graph, subject, DCTERMS.temporal,
#                            node_type=DCTERMS.PeriodOfTime)
