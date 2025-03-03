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

from pathlib import Path
from typing import List, Union

from pydantic import AnyHttpUrl, ConfigDict, Field
from rdflib.namespace import ODRL2

from sempyro import RDFModel


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
        json_schema_extra={
            "rdf_term": ODRL2.conflict,
            "rdf_type": "uri"
        }
    )
    permission: List[Union[AnyHttpUrl, RDFModel]] = Field(
        default=None,
        description="Permissions take preference over prohibitions.",
        json_schema_extra={
            "rdf_term": ODRL2.permission,
            "rdf_type": "uri"
        }
    )
    prohibition: List[Union[AnyHttpUrl, RDFModel]] = Field(
        default=None,
        description="The inability to perform an Action over an Asset.",
        json_schema_extra={
            "rdf_term": ODRL2.prohibition,
            "rdf_type": "uri"
        }
    )
    inheritFrom: List[AnyHttpUrl] = Field(
        default=None,
        description="Relates a (child) policy to another (parent) policy from which terms are inherited.",
        json_schema_extra={
            "rdf_term": ODRL2.inheritFrom,
            "rdf_type": "uri"
        }
    )
    profile: List[AnyHttpUrl] = Field(
        default=None,
        description="The identifier(s) of an ODRL Profile that the Policy conforms to.",
        json_schema_extra={
            "rdf_term": ODRL2.profile,
            "rdf_type": "uri"
        }
    )
    obligation: List[AnyHttpUrl] = Field(
        default=None,
        description="Relates an individual Duty to a Policy.",
        json_schema_extra={
            "rdf_term": ODRL2.obligation,
            "rdf_type": "uri"
        }
    )
    uid: List[AnyHttpUrl] = Field(
        default=None,
        description="Unique Identifier",
        json_schema_extra={
            "rdf_term": ODRL2.uid,
            "rdf_type": "uri"
        }
    )
    relation: List[AnyHttpUrl] = Field(
        default=None,
        description="Relation is an abstract property which creates an explicit link between an Action and an Asset.",
        json_schema_extra={
            "rdf_term": ODRL2.relation,
            "rdf_type": "uri"
        }
    )
    target: List[AnyHttpUrl] = Field(
        default=None,
        description="The target property indicates the Asset that is the primary subject to which the Rule action "
                    "directly applies.",
        json_schema_extra={
            "rdf_term": ODRL2.target,
            "rdf_type": "uri"
        }
    )
    function: List[AnyHttpUrl] = Field(
        default=None,
        description="Function is an abstract property whose sub-properties define the functional roles which may be "
                    "fulfilled by a party in relation to a Rule.",
        json_schema_extra={
            "rdf_term": ODRL2.function,
            "rdf_type": "uri"
        }
    )
    action: List[AnyHttpUrl] = Field(
        default=None,
        description="The operation relating to the Asset for which the Rule is being subjected.",
        json_schema_extra={
            "rdf_term": ODRL2.action,
            "rdf_type": "uri"
        }
    )
    constraint: List[AnyHttpUrl] = Field(
        default=None,
        description="Constraint applied to a Rule",
        json_schema_extra={
            "rdf_term": ODRL2.constraint,
            "rdf_type": "uri"
        }
    )
    assignee: List[AnyHttpUrl] = Field(
        default=None,
        description="The Party is the recipient of the Rule.",
        json_schema_extra={
            "rdf_term": ODRL2.assignee,
            "rdf_type": "uri"
        }
    )
    assigner: List[AnyHttpUrl] = Field(
        default=None,
        description="The Party is the issuer of the Rule.",
        json_schema_extra={
            "rdf_term": ODRL2.assigner,
            "rdf_type": "uri"
        }
    )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "odrl")
    ODRLPolicy.save_schema_to_file(path=Path(json_models_folder, "ODRLPolicy.json"),
                                   file_format="json")
    ODRLPolicy.save_schema_to_file(path=Path(json_models_folder, "ODRLPolicy.yaml"),
                                   file_format="yaml")
