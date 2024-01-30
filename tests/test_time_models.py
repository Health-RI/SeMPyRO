import json

import pytest

from pathlib import Path
from pydantic_core import ValidationError
from dcat.dcat_time_models import TimePosition, GeneralDateTimeDescription, DateTimeDescription, Greg, DayOfWeek
from rdflib import Graph, DCAT, Namespace, RDF, DCTERMS, TIME, URIRef
from rdflib.compare import to_isomorphic

TEST_DATA_DIRECTORY = Path(Path(__file__).parent.resolve(), "test_data")

EX = Namespace("http://www.example.com/")


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

def test_general_date_time_descr():
    with open(Path(TEST_DATA_DIRECTORY, "general_date_time_description.json"), "r") as test_data_file:
        assert GeneralDateTimeDescription.model_validate_json(test_data_file.read())


def test_general_date_time_descr_serialize():
    with open(Path(TEST_DATA_DIRECTORY, "general_date_time_description.json"), "r") as test_data_file:
        obj = GeneralDateTimeDescription.model_validate_json(test_data_file.read())
    dbr = Namespace("https://dbpedia.org/page/")
    graph = Graph()
    graph.bind("ex", EX)
    graph.bind("dbr", dbr)
    graph.bind("time", TIME)
    #todo bind namepace if not bound
    obj.to_graph_node(graph=graph,
                      subject=URIRef(EX),
                      node_predicate=EX.AbbyBirthdayHebrew,
                      node_type=TIME.GeneralDateTimeDescription)
    expected = Graph().parse(Path(TEST_DATA_DIRECTORY, "general_date_time_descr_example.ttl"))
    assert to_isomorphic(expected) == to_isomorphic(graph)


def test_date_time_descr():
    with open(Path(TEST_DATA_DIRECTORY, "date_time_description.json"), "r") as test_data_file:
        assert DateTimeDescription.model_validate_json(test_data_file.read())


def test_raises_at_hastrs_change():
    with pytest.raises(ValidationError):
        DateTimeDescription(dayOfWeek=DayOfWeek.Monday,
                            unitType=TIME.generalDay,
                            hasTRS="http://dbpedia.org/resource/Unix_time")


def test_date_time_descr_serialize():
    with open(Path(TEST_DATA_DIRECTORY, "date_time_description.json"), "r") as test_data_file:
        obj = DateTimeDescription.model_validate_json(test_data_file.read())
    graph = Graph()
    graph.bind("ex", EX)
    graph.bind("greg", Greg)
    graph.bind("time", TIME)
    obj.to_graph_node(graph=graph,
                      subject=URIRef(EX),
                      node_predicate=EX.AbbyBirthdayGregorian,
                      node_type=TIME.DateTimeDescription)
    expected = Graph().parse(Path(TEST_DATA_DIRECTORY, "date_time_description.ttl"))
    assert to_isomorphic(expected) == to_isomorphic(graph)
