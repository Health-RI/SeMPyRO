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
import logging
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Type, Union
from typing import Literal as typing_Literal

import ruamel.yaml
from pydantic import (
    AnyUrl,
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    NaiveDatetime,
    field_validator,
    model_validator,
)
from pydantic.fields import PydanticUndefined
from rdflib import XSD, BNode, Graph, Literal, URIRef
from rdflib.namespace import RDF, DefinedNamespaceMeta

from sempyro.utils.constants import year_month_pattern, year_pattern

RDF_KEY = "rdf_term"
RDF_TYPE_KEY = "rdf_type"
BIND_NAMESPACE_KEY = "bind_namespace"

logger = logging.getLogger("__name__")


class ModelAnnotationUtil:
    """A util class for quick access to RDFModel fields info"""
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
        if sys.version_info < (3, 10):
            logger.warning("This functionality can cause errors on Python 3.9, see issue 43 on Github.")
        return {key: {"datatype": self._get_list_types(datatype=value.annotation),
                      "RDF type": value.json_schema_extra.get("rdf_type", "No RDF type specified for the field")} for
                key, value in self.fields.items()}

    def fields_defaults(self):
        # if default is not set in a model it is PydanticUndefined
        return {key: value.default for key, value in self.fields.items() if
                value.default not in [None, PydanticUndefined]}

    def _get_list_types(self, datatype):
        dt_name = datatype.__name__
        if dt_name in ["List", "Union"]:
            types = []
            for subtype in datatype.__args__:
                types.append(self._get_list_types(subtype))
            return f"{dt_name}[{', '.join(types)}]"
        elif dt_name == "Annotated":
            return datatype.__args__[0].__name__
        else:
            return dt_name


class LiteralField(BaseModel):
    """
    Model to handle literal fields
    Attributes
    ----------
    datatype : str, pydantic.AnyUrl Optional
        datatype for literal value e.g. 'xsd:date' see https://www.w3.org/TR/xmlschema-2/#built-in-datatypes
    language : str Optional
        RFC 3066 language tag, see https://datatracker.ietf.org/doc/html/rfc3066.html, and also IANA-administrated 
        namespace of language tags: https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry
    value : str
        literal value
    either datatype or language, or none of these two attributes should be provided 
    as per http://www.w3.org/TR/rdf-concepts/#section-Graph-Literal
    """
    datatype: Union[AnyUrl, str] = Field(default=None, description="datatype,"
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
        if isinstance(data, dict):
            if data.get("datatype") and data.get("language"):
                raise ValueError("A Literal can only have one of 'language' or 'datatype', "
                                "per http://www.w3.org/TR/rdf-concepts/#section-Graph-Literal")
        return data

    @field_validator("datatype", mode="before")
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
        datatype = None
        if self.datatype:
            datatype = URIRef(self.datatype)
        value = Literal(self.value, lang=self.language, datatype=datatype)
        graph.add((subject, node_predicate, value))
        return graph


class RDFModelError(AttributeError):
    """An error thrown in case of incorrect defined model"""


class RDFModel(BaseModel):
    """Base class for creating pydantic models convertible to RDF graph"""
    model_config = ConfigDict(extra="forbid",
                              use_enum_values=True,
                              arbitrary_types_allowed=True,
                              validate_assignment=True
                              )

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
        graph.add((subject, RDF.type, URIRef(self.model_config["json_schema_extra"]["$IRI"])))
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
                bind_namespace = self.model_fields[field].json_schema_extra.get(BIND_NAMESPACE_KEY)
                if not isinstance(value, List):
                    value = [value]
                for item in value:
                    if issubclass(type(item), RDFModel):
                        item.to_graph_node(graph=graph,
                                           subject=node_to_add,
                                           node_predicate=rdf_predicate,
                                           node_type=item.model_config["json_schema_extra"]["$IRI"])
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
                    if bind_namespace:
                        graph.bind(bind_namespace[0], URIRef(bind_namespace[1]))

    @staticmethod
    def _convert_to_datetime_literal(value: Union[str, date, datetime, AwareDatetime, NaiveDatetime]) -> Literal:
        literal_format = None
        if isinstance(value, (datetime, AwareDatetime, NaiveDatetime)):
            literal_format = XSD.dateTime
            value = value.isoformat()
        elif isinstance(value, date):
            literal_format = XSD.date
            value = value.isoformat()
        elif isinstance(value, str):
            if re.match(year_month_pattern, value):
                literal_format = XSD.gYearMonth
            elif re.match(year_pattern, value):
                literal_format = XSD.gYear
            else:
                logging.warning(f"{str} does not match neither gYear nor gYearMonth pattern")
        else:
            raise TypeError(f"Value {value} is of unsupported type {type(value)}, either str, date, datetime, "
                            f"pydantic.AwareDatetime or pydantic.NaiveDatetime are expected")
        return Literal(value, datatype=literal_format)

    def _convert_to_rdf_type(self, rdf_type: str, value: Any) -> Union[URIRef, Literal]:
        if rdf_type.startswith("xsd:"):
            xsd_attribute = getattr(XSD, rdf_type.split(":")[-1])
            return Literal(value, datatype=xsd_attribute)
        if rdf_type == "literal":
            return Literal(value)
        elif rdf_type == "uri":
            return URIRef(str(value))
        elif rdf_type == "rdfs_literal":
            return Literal(value)
        elif rdf_type == "datetime_literal":
            return self._convert_to_datetime_literal(value)
        else:
            raise RDFModelError(f"{rdf_type} does not match any of allowed types.\n"
                                f"Expected types: 'literal', 'uri' or one of XSD types formatted `xsd:<type>`")

    @classmethod
    def annotate_model(cls):
        fields_definitions = ModelAnnotationUtil(cls)
        return fields_definitions

    @classmethod
    def save_schema_to_file(cls, path: Union[str, Path], file_format: typing_Literal["json", "yaml", "yml"] = None):
        if file_format is None:
            logger.warning("No format provided, assuming json")
            file_format = "json"
        elif file_format == "yml":
            file_format = "yaml"
        elif file_format not in ["yaml", "json"]:
            raise TypeError(f"Incorrect file format {file_format}, either 'json' or 'yaml expected")
        try:
            model_schema = cls.model_json_schema()
            saving_function = getattr(cls, f"_save_to_{file_format}")
            saving_function(path=path, model_schema=model_schema)
        except (FileNotFoundError, TypeError, AttributeError) as e:
            logger.error(f"Following error occurred while saving model to file: {e}")

    @classmethod
    def _save_to_json(cls, path: Union[str, Path], model_schema: Dict):
        with open(path, "w") as schema_file:
            json.dump(model_schema, schema_file, indent=2)

    @classmethod
    def _save_to_yaml(cls, path: Union[str, Path], model_schema: Dict):
        yaml = ruamel.yaml.YAML()
        with open(path, "w") as schema_yaml:
            model_schema = {key: (str(value) if isinstance(value, (URIRef, DefinedNamespaceMeta)) else value) for
                            key, value in model_schema.items()}
            new_defs = {}
            for def_model_name, def_model_json in (model_schema.get("$defs") or {}).items():
                new_model_json = {k: (str(v) if isinstance(v, (URIRef, DefinedNamespaceMeta)) else v) for
                                  k, v in def_model_json.items()}
                new_defs[def_model_name] = new_model_json
            model_schema["$defs"] = new_defs
            yaml.dump(model_schema, schema_yaml)
