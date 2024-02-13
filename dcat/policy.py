import logging

import json
from pathlib import Path
from pydantic import ConfigDict, Field, AnyHttpUrl
from typing import List, Union

from rdflib.namespace import ODRL2

from dcat.rdf_model import RDFModel

logger = logging.getLogger("__name__")


class ODRLPolicy(RDFModel):
    model_config = ConfigDict(title=ODRL2.Policy)

    conflict: List[Union[AnyHttpUrl, RDFModel]] = Field(
        default=None,
        description="The conflict-resolution strategy for a Policy.",
        rdf_term=ODRL2.conflict,
        rdf_type="uri"
    )
    permission: List[Union[AnyHttpUrl, RDFModel]] = Field(
        default=None,
        description="Permissions take preference over prohibitions.",
        rdf_term=ODRL2.permission,
        rdf_type="uri")
    prohibition: List[Union[AnyHttpUrl, RDFModel]] = Field(
        default=None,
        description="The inability to perform an Action over an Asset.",
        rdf_term=ODRL2.prohibition,
        rdf_type="uri")
    inheritFrom: List[AnyHttpUrl] = Field(
        default=None,
        description="Relates a (child) policy to another (parent) policy from which terms are inherited.",
        rdf_term=ODRL2.inheritFrom,
        rdf_type="uri")
    profile: List[AnyHttpUrl] = Field(
        default=None,
        description="The identifier(s) of an ODRL Profile that the Policy conforms to.",
        rdf_term=ODRL2.profile, rdf_type="uri")
    obligation: List[AnyHttpUrl] = Field(
        default=None,
        description="Relates an individual Duty to a Policy.",
        rdf_term=ODRL2.obligation, rdf_type="uri")
    uid: List[AnyHttpUrl] = Field(
        default=None,
        description="Unique Identifier",
        rdf_term=ODRL2.uid,
        rdf_type="uri")
    relation: List[AnyHttpUrl] = Field(
        default=None,
        description="Relation is an abstract property which creates an explicit link between an Action and an Asset.",
        rdf_term=ODRL2.relation,
        rdf_type="uri")
    target: List[AnyHttpUrl] = Field(
        default=None,
        description="The target property indicates the Asset that is the primary subject to which the Rule action "
                    "directly applies.",
        rdf_term=ODRL2.target,
        rdf_type="uri")
    # function: List[AnyHttpUrl, Any] = Field(default=None, description="", rdf_term=ODRL2.function, rdf_type="uri")
    # action: List[AnyHttpUrl, Any] = Field(default=None, description="", rdf_term=ODRL2.action, rdf_type="uri")
    # constraint: List[AnyHttpUrl, Any] = Field(default=None, description="", rdf_term=ODRL2.constraint, rdf_type="uri")
    # assignee: List[AnyHttpUrl, Any] = Field(default=None, description="", rdf_term=ODRL2.assignee, rdf_type="uri")
    # assigner: List[AnyHttpUrl, Any] = Field(default=None, description="", rdf_term=ODRL2.assigner, rdf_type="uri")


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parent.resolve(), "json_models")
    with open(Path(json_models_folder, "ODRLPolicy.json"), "w") as schema_file:
        model_schema = ODRLPolicy.model_json_schema()
        json.dump(model_schema, schema_file, indent=2)
