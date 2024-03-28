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

import pytest

from pathlib import Path
from pydantic_core import ValidationError, Url
from sempyro.vcard import VCard, VCARD
from sempyro.foaf import Agent
from sempyro import LiteralField
from rdflib import Graph, DCAT, Namespace, RDF, DCTERMS, URIRef
from rdflib.compare import to_isomorphic

TEST_DATA_DIRECTORY = Path(Path(__file__).parent.resolve(), "test_data")
MODELS_JSON_DIRECTORY = Path(Path(__file__).parents[1].resolve(), "models")

EX = Namespace("http://www.example.com/")


@pytest.mark.parametrize("model_name,test_path",
                         [("VCard", "vcard"),
                          ("Agent", "foaf")])
def test_vcard_agent(model_name, test_path):
    with open(Path(MODELS_JSON_DIRECTORY, test_path, f"{model_name}.json"), "r") as model_file:
        model_json = json.load(model_file)
    instance = globals()[model_name]
    actual_schema = instance.model_json_schema()
    assert json.dumps(model_json) == json.dumps(actual_schema)


@pytest.mark.parametrize("email", ["mailto:exampleemail@domain.com",
                                   "mailto://exampleemail@domain.com",
                                   "exampleemail@domain.com",
                                   ["exampleemail@domain.com"]
                                   ])
def test_vcard_email(email):
    card_obj = VCard(hasEmail=email, full_name=["I am example"], hasUID="https://orcid.org/0009-0000-xxxx-xxxx")
    expected = [Url("mailto:exampleemail@domain.com")]
    assert card_obj.hasEmail == expected


@pytest.mark.parametrize("email", ["my:email@gmail.com",
                                   "myemailgmail.com",
                                   "mailto:emailgmail.com"])
def test_vcard_email_validation(email):
    with pytest.raises(ValidationError):
        card_obj = VCard(hasEmail=email,
                         full_name=["I am example"],
                         hasUID="https://orcid.org/0009-0000-xxxx-xxxx")


def test_vcard_serialization():
    names = [LiteralField(value="Emir Kusturica", language="en"),
             LiteralField(value="Емир Кустурица", language="sr")]
    film_director = VCard(hasEmail="exampleemail@domain.com",
                          full_name=names,
                          hasUID="https://en.wikipedia.org/wiki/Emir_Kusturica")
    actual_graph = film_director.to_graph(URIRef("http:example.com/Emir_Kusturica"))
    expected_graph = Graph().parse(Path(TEST_DATA_DIRECTORY, "vCard.ttl"))
    assert to_isomorphic(actual_graph) == to_isomorphic(expected_graph)
    assert [x for x in actual_graph.namespaces()] == [y for y in expected_graph.namespaces()]


def test_agent():
    person = Agent(name=["Jorrit H. Poelen"], identifier="https://dcat.example.org/PoelenJorritHID")
    actual_graph = person.to_graph(subject=URIRef("https://dcat.example.org/PoelenJorritHID"))
    expected_graph = Graph().parse(Path(TEST_DATA_DIRECTORY, "agent.ttl"))
    assert to_isomorphic(actual_graph) == to_isomorphic(expected_graph)


def test_vcard_namespace():
    actual_graph = Graph()
    example_ns = Namespace("http://www.example.com/")
    subject = example_ns.MagicBus
    actual_graph.bind("ex", example_ns)
    actual_graph.add((subject, RDF.type, DCAT.Dataset))
    names = [LiteralField(value="Emir Kusturica", language="en"),
             LiteralField(value="Емир Кустурица", language="sr")]
    film_director = VCard(hasEmail="exampleemail@domain.com",
                          full_name=names,
                          hasUID="https://en.wikipedia.org/wiki/Emir_Kusturica")
    film_director.to_graph_node(graph=actual_graph,
                                subject=subject,
                                node_predicate=DCTERMS.creator,
                                node_type=VCARD.VCard)
    expected_graph = Graph()
    expected_graph.bind("ex", example_ns)
    expected_graph.bind("v", VCARD)
    expected_graph.parse(Path(TEST_DATA_DIRECTORY, "vCard_as_a_node.ttl"))
    assert to_isomorphic(actual_graph) == to_isomorphic(expected_graph)
    assert [x for x in actual_graph.namespaces()] == [y for y in expected_graph.namespaces()]
