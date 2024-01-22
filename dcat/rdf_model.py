import logging
from pydantic import BaseModel, ConfigDict
from pydantic.fields import PydanticUndefined
from typing import Union, Type
from rdflib import BNode, Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS

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


class RDFModelError(AttributeError):
    """An error thrown in case of incorrect defined model"""


class RDFModel(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True, arbitrary_types_allowed=True)

    def to_graph_node(self,
                      graph: Graph,
                      subject: Union[URIRef, BNode],
                      node_predicate: URIRef,
                      node_type: URIRef) -> Graph:
        rdf_field_types = {"literal": Literal, "uri": URIRef, "rdfs_literal": RDFS.Literal}
        node_to_add = BNode()
        graph.add((subject, node_predicate, node_to_add))
        graph.add((node_to_add, RDF.type, node_type))
        for field, value in iter(self):
            if value:
                rdf_predicate = self.model_fields[field].json_schema_extra[RDF_KEY]
                type_key = self.model_fields[field].json_schema_extra.get(RDF_TYPE_KEY)
                rdf_type = rdf_field_types.get(type_key, type_key)
                if issubclass(type(value), (BaseModel, RDFModel)):
                    # if rdf_type is None:
                    #     raise RDFModelError(f"rdf_type is not specified for {type(value)} model")
                    value.to_graph_node(graph=graph,
                                        subject=node_to_add,
                                        node_predicate=rdf_predicate,
                                        node_type=value.model_config["title"])
                else:
                    if rdf_type is None:
                        logger.warning(f"No {RDF_TYPE_KEY} provided in schema, that may cause errors")
                    else:
                        value = rdf_type(value)
                    graph.add((node_to_add, rdf_predicate, value))
        return graph

    @classmethod
    def annotate_model(cls):
        fields_definitions = ModelAnnotationUtil(cls)
        return fields_definitions
