import json

import pytest

from pathlib import Path
from pydantic_core import ValidationError, Url
from dcat.vcard import VCard, Agent, VCARD
from dcat.rdf_model import LiteralField
from rdflib import Graph, DCAT, Namespace, RDF, DCTERMS, TIME, URIRef, BNode
from rdflib.compare import to_isomorphic

TEST_DATA_DIRECTORY = Path(Path(__file__).parent.resolve(), "test_data")
MODELS_JSON_DIRECTORY = Path(Path(__file__).parents[1].resolve(), "dcat", "json_models")

EX = Namespace("http://www.example.com/")


@pytest.mark.parametrize("model_name", ["VCard",
                                        "Agent"])
def test_vcard_agent(model_name):
    with open(Path(MODELS_JSON_DIRECTORY, f"{model_name}.json"), "r") as model_file:
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

