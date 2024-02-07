from pydantic import AnyHttpUrl, ConfigDict, Field
from rdflib import PROV
from typing import Any, AnyStr, Union, List

from dcat.rdf_model import RDFModel, LiteralField


class Association(RDFModel):
    model_config = ConfigDict(title=PROV.Association)

    hadPlan: Union[AnyHttpUrl, Any] = Field(
        default=None,
        description="A plan is an entity that represents a set of actions or steps intended by one or more agents to "
                    "achieve some goals.",
        rdf_term=PROV.hadPlan,
        rdf_type="uri")
    hadRole: Union[AnyHttpUrl, Any] = Field(
        default=None,
        description="A role is the function of an entity or agent with respect to an activity, in the context of "
                    "a usage, generation, invalidation, association, start, and end.",
        rdf_term=PROV.hadRole)
    agent: Union[AnyHttpUrl, Any] = Field(
        default=None,
        description="The prov:agent property references an prov:Agent which influenced a resource. "
                    "This property applies to an prov:AgentInfluence, which is given by a subproperty of "
                    "prov:qualifiedInfluence from the influenced prov:Entity, prov:Activity or prov:Agent.",
        rdf_term=PROV.Agent,
        rdf_type="uri"
    )


class End(RDFModel):
    model_config = ConfigDict(title=PROV.End)

    hadActivity: Any = Field(default=None)
    atTime: Any = Field(default=None)
    entity: Any = Field(default=None)


class Activity(RDFModel):
    model_config = ConfigDict(title=PROV.Activity)

    generated: List[Any] = Field(
        default=None,
        description="Generation is the completion of production of a new entity by an activity. This entity did not "
                    "exist before generation and becomes available for usage after this generation.",
        rdf_term=PROV.generated,
        rdf_type="uri"
    )
    qualifiedAssociation: List[Association] = Field(
        default=None,
        description="An activity association is an assignment of responsibility to an agent for an activity, "
                    "indicating that the agent had a role in the activity. It further allows for a plan to be "
                    "specified, which is the plan intended by the agent to achieve some goals in the context of this "
                    "activity.",
        rdf_term=PROV.qualifiedQuotation,
        rdf_type=PROV.Association
    )
    wasAssociatedWith: Union[AnyHttpUrl, Any] = Field(
        default=None,
        description="An activity association is an assignment of responsibility to an agent for an activity, "
                    "indicating that the agent had a role in the activity. It further allows for a plan to be "
                    "specified, which is the plan intended by the agent to achieve some goals in the context of this "
                    "activity.",
        rdf_term=PROV.wasAssociatedWith,
        rdf_type="uri"
    )
    qualifiedEnd: End = Field(
        default=None,
        description="End is when an activity is deemed to have been ended by an entity, known as trigger. "
                    "The activity no longer exists after its end. Any usage, generation, or invalidation involving "
                    "an activity precedes the activity's end. An end may refer to a trigger entity that terminated "
                    "the activity, or to an activity, known as ender that generated the trigger.",
        rdf_term=PROV.qualifiedEnd,
        edf_type=PROV.End
    )
    wasEndedBy: Any = Field(default=None, description="", rdf_term=PROV.wasEndedBy)
    qualifiedUsage: Any = Field(default=None, description="", rdf_term=PROV.qualifiedUsage)
    used: Any = Field(default=None, description="", rdf_term=PROV.used)
    invalidated: Any = Field(default=None, description="", rdf_term=PROV.invalidated)
    endedAtTime: Any = Field(default=None, description="", rdf_term=PROV.endedAtTime)
    qualifiedStart: Any = Field(default=None, description="", rdf_term=PROV.qualifiedStart)
    wasInformedBy: Any = Field(default=None, description="", rdf_term=PROV.wasInformedBy)
    wasStartedBy: Any = Field(default=None, description="", rdf_term=PROV.wasStartedBy)
    startedAtTime: Any = Field(default=None, description="", rdf_term=PROV.startedAtTime)
    qualifiedCommunication: Any = Field(default=None, description="", rdf_term=PROV.qualifiedCommunication)
    wasInfluencedBy: Any = Field(default=None, description="", rdf_term=PROV.wasInfluencedBy)
    qualifiedInfluence: Any = Field(default=None, description="", rdf_term=PROV.qualifiedInfluence)
    atLocation: Any = Field(default=None, description="", rdf_term=PROV.atLocation)
