from pathlib import Path
from pydantic import ConfigDict, Field, AnyHttpUrl
from typing import List, Union

from rdflib.namespace import ODRL2

from dcat.rdf_model import RDFModel


class ODRLPolicy(RDFModel):
    """A non-empty group of Permissions and/or Prohibitions."""
    model_config = ConfigDict(
        json_schema_extra={
            "$ontology": "https://www.w3.org/TR/odrl-vocab/#",
            "$namespace": str(ODRL2),
            "$IRI": ODRL2.Policy,
            "$prefix": "odrl"
        }
    )

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
    function: List[AnyHttpUrl] = Field(
        default=None,
        description="Function is an abstract property whose sub-properties define the functional roles which may be "
                    "fulfilled by a party in relation to a Rule.",
        rdf_term=ODRL2.function,
        rdf_type="uri")
    action: List[AnyHttpUrl] = Field(
        default=None,
        description="The operation relating to the Asset for which the Rule is being subjected.",
        alias="hasAction",
        rdf_term=ODRL2.action,
        rdf_type="uri")
    constraint: List[AnyHttpUrl] = Field(
        default=None,
        description="Constraint applied to a Rule",
        rdf_term=ODRL2.constraint,
        rdf_type="uri")
    assignee: List[AnyHttpUrl] = Field(
        default=None,
        description="The Party is the recipient of the Rule.",
        rdf_term=ODRL2.assignee,
        rdf_type="uri")
    assigner: List[AnyHttpUrl] = Field(
        default=None,
        description="The Party is the issuer of the Rule.",
        rdf_term=ODRL2.assigner,
        rdf_type="uri")


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parent.resolve(), "json_models")
    ODRLPolicy.save_schema_to_file(path=Path(json_models_folder, f"ODRLPolicy.json"),
                                   file_format="json")
    ODRLPolicy.save_schema_to_file(path=Path(json_models_folder, f"ODRLPolicy.yaml"),
                                   file_format="yaml")
