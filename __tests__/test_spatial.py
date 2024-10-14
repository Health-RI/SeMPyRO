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
import sys
from pathlib import Path

import pytest
from rdflib import DCAT, DCTERMS, RDF, Graph, URIRef
from rdflib.compare import to_isomorphic

from sempyro import LiteralField
from sempyro.geo import Geometry, Location
from sempyro.namespaces import LOCN, GeoSPARQL

TEST_DATA_DIRECTORY = Path(Path(__file__).parent.resolve(), "test_data")
MODELS_JSON_DIRECTORY = Path(Path(__file__).parents[1].resolve(), "models", "geo")


@pytest.mark.parametrize("model_name", ["Location", "Geometry"])
def test_spatial_objects(model_name):
    with open(Path(MODELS_JSON_DIRECTORY, f"{model_name}.json")) as model_file:
        model_json = json.load(model_file)
    instance = globals()[model_name]
    actual_schema = instance.model_json_schema()
    assert json.dumps(model_json) == json.dumps(actual_schema)


@pytest.mark.xfail(sys.platform == "win32", reason="Different line endings Windows/*nix systems")
def test_spatial_ex29():
    expected_graph = Graph().parse(Path(TEST_DATA_DIRECTORY, "spatial_ex29.ttl"))

    actual_graph = Graph()
    subject = URIRef("http://example.com#AnneFrank_0")
    actual_graph.add((subject, RDF.type, DCAT.Dataset))
    actual_graph.bind("locn", LOCN)

    polygon_string = """POLYGON ((
      4.8842353 52.375108 , 4.884276 52.375153 ,
      4.8842567 52.375159 , 4.883981 52.375254 ,
      4.8838502 52.375109 , 4.883819 52.375075 ,
      4.8841037 52.374979 , 4.884143 52.374965 ,
      4.8842069 52.375035 , 4.884263 52.375016 ,
      4.8843200 52.374996 , 4.884255 52.374926 ,
      4.8843289 52.374901 , 4.884451 52.375034 ,
      4.8842353 52.375108
    ))"""
    geometry = LiteralField(value=polygon_string, datatype=GeoSPARQL.wktLiteral)
    location = Location(geometry=geometry)

    location.to_graph_node(graph=actual_graph,
                           subject=subject,
                           node_predicate=DCTERMS.spatial,
                           node_type=DCTERMS.Location)

    assert to_isomorphic(expected_graph) == to_isomorphic(actual_graph)
