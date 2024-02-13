import logging
from pydantic import BaseModel, ConfigDict, Field, model_validator, field_validator
from pydantic.fields import PydanticUndefined
from typing import Union, Type, Any, Dict, List
from rdflib import BNode, Graph, URIRef, Literal, XSD
from rdflib.namespace import RDF

RDF_KEY = "rdf_term"
RDF_TYPE_KEY = "rdf_type"

logger = logging.getLogger("__name__")


class ModelAnnotationUtil:
    def __init__(self, model: Union[Type[BaseModel]]):
        self.fields = model.model_fields

    def get_names(self):
        return list(self.fields.keys())

    def mandatory_fields(self):
        # if default is not set in a model it is PydanticUndefined
        return [x for x in self.fields.keys() if self.fields[x].default is not None]

    def fields_description(self):
        return {key: value.description for key, value in self.fields.items()}

    def get_rdf_correspondence(self):
        return {key: value.json_schema_extra.get("rdf_term", "No RDF term specified for the field") for key, value in
                self.fields.items()}

    def get_fields_types(self):
        return {key: {"datatype": value.annotation.__name__,
                      "RDF type": value.json_schema_extra.get("rdf_type", "No RDF type specified for the field")} for
                key, value in self.fields.items()}

    def fields_defaults(self):
        # if default is not set in a model it is PydanticUndefined
        return {key: value.default for key, value in self.fields.items() if
                value.default not in [None, PydanticUndefined]}


class LiteralField(BaseModel):
    """
    Model to handle literal fields
    Attributes
    ----------
    datatype : str Optional
        datatype for literal value e.g. 'xsd:date' see https://www.w3.org/TR/xmlschema-2/#built-in-datatypes
    language : str Optional
        RFC 3066 language tag, see https://datatracker.ietf.org/doc/html/rfc3066.html, and also IANA-administrated 
        namespace of language tags: https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry
    value : str
        literal value
    either datatype or language, or none of these two attributes should be provided 
    as per http://www.w3.org/TR/rdf-concepts/#section-Graph-Literal
    """
    datatype: str = Field(default=None, description="datatype,"
                                                    "see https://www.w3.org/TR/xmlschema-2/#built-in-datatypes")
    language: str = Field(default=None,
                          description="RFC 3066 language tag, see https://datatracker.ietf.org/doc/html/rfc3066.html,"
                                      "and also IANA-administrated namespace of language tags: "
                                      "https://www.iana.org/assignments/language-subtag-registry/language-subtag-"
                                      "registry")
    value: str = Field(description="Field value")

    @model_validator(mode="before")
    @classmethod
    def validate(cls, data: Dict) -> Dict[str, Any]:
        if data.get("datatype") and data.get("language"):
            raise ValueError("A Literal can only have one of 'language' or 'datatype', "
                             "per http://www.w3.org/TR/rdf-concepts/#section-Graph-Literal")
        return data

    @field_validator("datatype", mode='before')
    @classmethod
    def try_solve_datatype(cls, value: str) -> Union[str, URIRef]:
        """
        Tries to find a datatype in rdflib.XSD namespace
        """
        if value and value.startswith("xsd:"):
            xsd_attribute = getattr(XSD, value.split(":")[-1])
            if xsd_attribute is not None:
                return xsd_attribute
            else:
                logger.warning(f"{value} not found in XSD namespace")
        return value

    def flatten_to_literal(self, graph, subject, node_predicate):
        value = Literal(self.value, lang=self.language, datatype=self.datatype)
        graph.add((subject, node_predicate, value))
        return graph


class RDFModelError(AttributeError):
    """An error thrown in case of incorrect defined model"""


class RDFModel(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True, arbitrary_types_allowed=True)

    def to_graph_node(self,
                      graph: Graph,
                      subject: Union[URIRef, BNode],
                      node_predicate: URIRef,
                      node_type: Union[URIRef, List[URIRef]]) -> Graph:
        node_to_add = BNode()
        graph.add((subject, node_predicate, node_to_add))
        graph = self._check_and_add_namespaces(graph)
        if isinstance(node_type, URIRef):
            node_type = [node_type]
        for n_type in node_type:
            graph.add((node_to_add, RDF.type, n_type))
        self._add_fields_to_graph(graph=graph, node_to_add=node_to_add)
        return graph

    def to_graph(self, subject):
        graph = Graph(bind_namespaces="rdflib")
        graph.add((subject, RDF.type, URIRef(self.model_config["title"])))
        graph = self._check_and_add_namespaces(graph)
        self._add_fields_to_graph(graph=graph, node_to_add=subject)
        return graph

    def _check_and_add_namespaces(self, graph):
        if self.model_config["json_schema_extra"]["$namespace"] not in [x[1] for x in graph.namespaces()]:
            graph.bind(self.model_config["json_schema_extra"]["$prefix"],
                       self.model_config["json_schema_extra"]["$namespace"])
        return graph

    def _add_fields_to_graph(self, graph, node_to_add):
        for field, value in iter(self):
            if value:
                rdf_predicate = self.model_fields[field].json_schema_extra[RDF_KEY]
                rdf_type = self.model_fields[field].json_schema_extra.get(RDF_TYPE_KEY)
                if not isinstance(value, List):
                    value = [value]
                for item in value:
                    if issubclass(type(item), RDFModel):
                        item.to_graph_node(graph=graph,
                                           subject=node_to_add,
                                           node_predicate=rdf_predicate,
                                           node_type=item.model_config["title"])
                    elif issubclass(type(item), LiteralField):
                        item.flatten_to_literal(graph=graph,
                                                subject=node_to_add,
                                                node_predicate=rdf_predicate)
                    else:
                        if rdf_type is None:
                            logger.warning(f"No {RDF_TYPE_KEY} provided in schema, that may cause errors")
                        else:
                            item = self._convert_to_rdf_type(rdf_type, item)
                        graph.add((node_to_add, rdf_predicate, item))

    @staticmethod
    def _convert_to_rdf_type(rdf_type: str, value: Any) -> Union[URIRef, Literal]:
        if rdf_type.startswith("xsd:"):
            xsd_attribute = getattr(XSD, rdf_type.split(":")[-1])
            return Literal(value, datatype=xsd_attribute)
        match rdf_type:
            case "literal":
                return Literal(value)
            case "uri":
                return URIRef(str(value))
            case "rdfs_literal":
                return Literal(value)
            case _:
                raise RDFModelError(f"{rdf_type} does not match any of allowed types.\n"
                                    f"Expected types: 'literal', 'uri' or one of XDS types formatted `xsd:<type>`")

    @classmethod
    def annotate_model(cls):
        fields_definitions = ModelAnnotationUtil(cls)
        return fields_definitions
