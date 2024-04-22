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
from pydantic_core import ValidationError
from rdflib import DCAT, DCTERMS, RDF, TIME, BNode, Graph, Namespace, URIRef
from rdflib.compare import to_isomorphic

from sempyro import LiteralField
from sempyro.namespaces import Greg
from sempyro.time import (
    DateTimeDescription,
    DayOfWeek,
    GeneralDateTimeDescription,
    PeriodOfTime,
    TimeInstant,
    TimePosition,
)

TEST_DATA_DIRECTORY = Path(Path(__file__).parent.resolve(), "test_data")
MODELS_JSON_DIRECTORY = Path(Path(__file__).parents[1].resolve(), "models", "time")

EX = Namespace("http://www.example.com/")


@pytest.mark.parametrize("model_name", ["TimePosition",
                                        "GeneralDateTimeDescription",
                                        "DateTimeDescription",
                                        "TimeInstant",
                                        "PeriodOfTime"])
def test_time_models(model_name):
    with open(Path(MODELS_JSON_DIRECTORY, f"{model_name}.json")) as model_file:
        model_json = json.load(model_file)
    instance = globals()[model_name]
    actual_schema = instance.model_json_schema()
    assert json.dumps(model_json) == json.dumps(actual_schema)


@pytest.mark.parametrize("input_file", ["time_position_nominal.json", "time_position_numeric.json"])
def test_time_position(input_file):
    with open(Path(TEST_DATA_DIRECTORY, input_file)) as file:
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


def test_time_position_to_graph():
    """Test TimePosition serialization to a graph node """
    time_position_start = TimePosition(hasTRS="http://resource.geosciml.org/classifier/cgi/geologicage/ma",
                                       numericPosition=541.0)
    time_position_end = TimePosition(hasTRS="http://resource.geosciml.org/classifier/cgi/geologicage/ma",
                                     numericPosition=251.902)
    graph = Graph()
    subject = EX.ds850
    graph.bind("ex", EX)
    graph.add((subject, RDF.type, DCAT.Dataset))
    temporal_node = BNode()
    graph.add((subject, DCTERMS.temporal, temporal_node))
    graph.add((temporal_node, RDF.type, DCTERMS.PeriodOfTime))
    graph.add((temporal_node, RDF.type, TIME.ProperInterval))
    start_time_instant_node = BNode()
    graph.add((temporal_node, TIME.hasBeginning, start_time_instant_node))
    graph.add((start_time_instant_node, RDF.type, TIME.Instant))
    time_position_start.to_graph_node(graph=graph,
                                      subject=start_time_instant_node,
                                      node_predicate=TIME.inTimePosition,
                                      node_type=TIME.TimePosition)
    end_time_instant_node = BNode()
    graph.add((temporal_node, TIME.hasEnd, end_time_instant_node))
    graph.add((end_time_instant_node, RDF.type, TIME.Instant))
    time_position_end.to_graph_node(graph=graph,
                                    subject=end_time_instant_node,
                                    node_predicate=TIME.inTimePosition,
                                    node_type=TIME.TimePosition)
    expected_graph = Graph().parse(Path(TEST_DATA_DIRECTORY, "example_26.ttl"))
    assert to_isomorphic(expected_graph) == to_isomorphic(graph)


def test_general_date_time_descr():
    with open(Path(TEST_DATA_DIRECTORY, "general_date_time_description.json")) as test_data_file:
        assert GeneralDateTimeDescription.model_validate_json(test_data_file.read())


def test_general_date_time_descr_serialize():
    with open(Path(TEST_DATA_DIRECTORY, "general_date_time_description.json")) as test_data_file:
        obj = GeneralDateTimeDescription.model_validate_json(test_data_file.read())
    dbr = Namespace("https://dbpedia.org/page/")
    graph = Graph()
    graph.bind("ex", EX)
    graph.bind("dbr", dbr)
    graph.bind("time", TIME)
    obj.to_graph_node(graph=graph,
                      subject=URIRef(EX),
                      node_predicate=EX.AbbyBirthdayHebrew,
                      node_type=TIME.GeneralDateTimeDescription)
    expected = Graph().parse(Path(TEST_DATA_DIRECTORY, "general_date_time_descr_example.ttl"))
    assert to_isomorphic(expected) == to_isomorphic(graph)


def test_date_time_descr():
    with open(Path(TEST_DATA_DIRECTORY, "date_time_description.json")) as test_data_file:
        assert DateTimeDescription.model_validate_json(test_data_file.read())


def test_raises_at_hastrs_change():
    with pytest.raises(ValidationError):
        DateTimeDescription(dayOfWeek=DayOfWeek.Monday,
                            unitType=TIME.generalDay,
                            hasTRS="http://dbpedia.org/resource/Unix_time")


def test_date_time_descr_serialize():
    with open(Path(TEST_DATA_DIRECTORY, "date_time_description.json")) as test_data_file:
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


@pytest.mark.parametrize("data",
                         (
                                 # start and stop dates as strings
                                 {
                                     "start_date": "2016-03-04",
                                     "end_date": "2018-08-05"
                                 },
                                 # start and stop dates as LiteralField
                                 {
                                     "start_date": {
                                         "value": "2016-03-04",
                                         "datatype": "xsd:date"
                                     },
                                     "end_date": {
                                         "value": "2018-08-05",
                                         "datatype": "xsd:date"
                                     }
                                 },
                                 # open intervals defined with start and stop dates
                                 {
                                     "end_date": "2016-03-04"
                                 },
                                 {
                                     "start_date": {
                                         "value": "2016",
                                         "datatype": "xsd:gYear"
                                     }
                                 },
                                 # beginning and end to define an interval
                                 {
                                     "beginning": {
                                         "inXSDgYear": "1914"
                                     },
                                     "end": {
                                         "inXSDgYear": "1939"
                                     }
                                 },
                                 # beginning open interval
                                 {
                                     "beginning": {
                                         "inXSDDate": "2016-03-04"
                                     }
                                 }
                         ))
def test_period_of_time(data):
    assert PeriodOfTime.model_validate_json(json.dumps(data))


@pytest.mark.parametrize("data",
                         ({
                              "start_date": "2016-03-04",
                              "beginning": {
                                  "inXSDDate": "2016-03-04"
                              }
                          },
                          {
                              "start_date": "2016-03-04",
                              "end": {
                                  "inXSDgYear": "1939"
                              }
                          },
                          {
                              "end_date": {
                                  "value": "2018-08-05",
                                  "datatype": "xsd:date"
                              },
                              "end": {
                                  "inXSDgYear": "1939"}
                          }
                         )
                         )
def test_period_of_time_validation(data):
    with pytest.raises(ValidationError):
        PeriodOfTime.model_validate_json(json.dumps(data))


def test_period_of_time_ex23():
    expected_graph = Graph().parse(Path(TEST_DATA_DIRECTORY, "period_of_time_ex23.ttl"))
    period_of_time = PeriodOfTime(start_date=LiteralField(value="2016-03-04", datatype="xsd:date"),
                                  end_date=LiteralField(value="2018-08-05", datatype="xsd:date"))
    actual_graph = Graph()
    subject = EX.ds257
    actual_graph.bind("ex", EX)
    actual_graph.add((subject, RDF.type, DCAT.Dataset))
    period_of_time.to_graph_node(graph=actual_graph,
                                 subject=subject,
                                 node_predicate=DCTERMS.temporal,
                                 node_type=DCTERMS.PeriodOfTime)
    assert to_isomorphic(expected_graph) == to_isomorphic(actual_graph)


def test_period_of_time_ex24():
    expected_graph = Graph().parse(Path(TEST_DATA_DIRECTORY, "period_of_time_ex24.ttl"))
    period_of_time = PeriodOfTime(beginning=TimeInstant(inXSDDate="2016-03-04"),
                                  end=TimeInstant(inXSDDate="2018-08-05"))
    actual_graph = Graph()
    subject = EX.ds348
    actual_graph.bind("ex", EX)
    actual_graph.add((subject, RDF.type, DCAT.Dataset))
    period_of_time.to_graph_node(graph=actual_graph,
                                 subject=subject,
                                 node_predicate=DCTERMS.temporal,
                                 node_type=[DCTERMS.PeriodOfTime, TIME.ProperInterval])
    assert to_isomorphic(expected_graph) == to_isomorphic(actual_graph)


def test_period_of_time_ex26():
    """Test PeriodOfTime and TimeInstant serialization to a graph node"""
    expected_graph = Graph().parse(Path(TEST_DATA_DIRECTORY, "example_26.ttl"))
    time_position_start = TimePosition(hasTRS="http://resource.geosciml.org/classifier/cgi/geologicage/ma",
                                       numericPosition=541.0)
    time_position_end = TimePosition(hasTRS="http://resource.geosciml.org/classifier/cgi/geologicage/ma",
                                     numericPosition=251.902)
    start_time_instant = TimeInstant(inTimePosition=time_position_start)
    end_time_instant = TimeInstant(inTimePosition=time_position_end)
    period_of_time = PeriodOfTime(beginning=start_time_instant, end=end_time_instant)
    actual_graph = Graph()
    subject = EX.ds850
    actual_graph.bind("ex", EX)
    actual_graph.add((subject, RDF.type, DCAT.Dataset))
    period_of_time.to_graph_node(graph=actual_graph,
                                 subject=subject,
                                 node_predicate=DCTERMS.temporal,
                                 node_type=[DCTERMS.PeriodOfTime, TIME.ProperInterval])
    assert to_isomorphic(expected_graph) == to_isomorphic(actual_graph)


@pytest.mark.parametrize("data", (
        {"inXSDDate": "2023-08-08"},
        {"inXSDDateTimeStamp": "2023-08-08T15:32:00Z"},
        {"inXSDgYear": "1990"},
        {"inXSDgYearMonth": "2008-08+03:09"},
        {"inXSDgYearMonth": "2008-08Z"},
        {"inTimePosition": {"hasTRS": "http://resource.geosciml.org/classifier/cgi/geologicage/ma",
                            "numericPosition": 541.0}},
        {"inDateTime": {
            "day": "---23",
            "dayOfWeek": "http://www.w3.org/2006/time#Wednesday",
            "dayOfYear": "143",
            "hour": "8",
            "minute": "20",
            "hasTRS": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian",
            "month": "--05",
            "monthOfYear": "http://www.w3.org/ns/time/gregorian#May",
            "timeZone": "https://www.timeanddate.com/time/zones/awst",
            "unitType": "http://www.w3.org/2006/time#unitMinute",
            "year": "2001"
        }
        }
))
def test_time_instant(data):
    assert TimeInstant.model_validate_json(json.dumps(data))


def test_time_instant_validation():
    with pytest.raises(ValidationError):
        data = {"inXSDDate": "2023-08-08",
                "inXSDDateTimeStamp": "2023-08-08T15:32:00Z"}
        assert TimeInstant.model_validate_json(json.dumps(data))
