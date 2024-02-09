from pydantic import AnyHttpUrl, ConfigDict, Field, NaiveDatetime, AwareDatetime
from rdflib import PROV
from typing import Union, List

from dcat.rdf_model import RDFModel


class Association(RDFModel):
    model_config = ConfigDict(title=PROV.Association)

    hadPlan: Union[AnyHttpUrl, RDFModel] = Field(
        default=None,
        description="A plan is an entity that represents a set of actions or steps intended by one or more agents to "
                    "achieve some goals.",
        rdf_term=PROV.hadPlan,
        rdf_type="uri")
    hadRole: Union[AnyHttpUrl, RDFModel] = Field(
        default=None,
        description="A role is the function of an entity or agent with respect to an activity, in the context of "
                    "a usage, generation, invalidation, association, start, and end.",
        rdf_term=PROV.hadRole,
        rdf_type="uri"
    )
    agent: Union[AnyHttpUrl, RDFModel] = Field(
        default=None,
        description="The prov:agent property references an prov:Agent which influenced a resource. "
                    "This property applies to an prov:AgentInfluence, which is given by a subproperty of "
                    "prov:qualifiedInfluence from the influenced prov:Entity, prov:Activity or prov:Agent.",
        rdf_term=PROV.Agent,
        rdf_type="uri"
    )


class InstantaneousEvent(RDFModel):
    model_config = ConfigDict(title=PROV.InstantaneousEvent)

    atTime: Union[NaiveDatetime, AwareDatetime] = Field(
        default=None,
        description="The PROV data model is implicitly based on a notion of instantaneous events (or just events), "
                    "that mark transitions in the world. Events include generation, usage, or invalidation of entities,"
                    " as well as starting or ending of activities. This notion of event is not first-class in the data "
                    "model, but it is useful for explaining its other concepts and its semantics.",
        rdf_term=PROV.InstantaneousEvent,
        rdf_type="xsd:dateTime"
    )
    hadRole: Union[AnyHttpUrl, RDFModel] = Field(
        default=None,
        description="A role is the function of an entity or agent with respect to an activity, in the context of "
                    "a usage, generation, invalidation, association, start, and end.",
        rdf_term=PROV.hadRole,
        rdf_type="uri"
    )
    atLocation: Union[AnyHttpUrl, RDFModel] = Field(
        default=None,
        description="A location can be an identifiable geographic place (ISO 19112), but it can also be a "
                    "non-geographic place such as a directory, row, or column. As such, there are numerous ways in "
                    "which location can be expressed, such as by a coordinate, address, landmark, and so forth.",
        rdf_term=PROV.atLocation,
        rdf_type="uri"
    )


class EntityInfluence(RDFModel):
    model_config = ConfigDict(title=PROV.EntityInfluence)

    entity: AnyHttpUrl = Field(
        default=None,
        description="The prov:entity property references an prov:Entity which influenced a resource. This property "
                    "applies to an prov:EntityInfluence, which is given by a subproperty of prov:qualifiedInfluence "
                    "from the influenced prov:Entity, prov:Activity or prov:Agent.",
        rdf_term=PROV.Entity,
        rdf_type="uri"
    )
    hadRole: Union[AnyHttpUrl, RDFModel] = Field(
        default=None,
        description="A role is the function of an entity or agent with respect to an activity, in the context of "
                    "a usage, generation, invalidation, association, start, and end.",
        rdf_term=PROV.hadRole,
        rdf_type="uri"
    )
    influencer: AnyHttpUrl = Field(
        default=None,
        description="This property is used as part of the qualified influence pattern. Subclasses of prov:Influence "
                    "use these subproperties to reference the resource (Entity, Agent, or Activity) whose influence is "
                    "being qualified.",
        rdf_term=PROV.influencer,
        rdf_type="uri"
    )
    hadActivity: AnyHttpUrl = Field(
        default=None,
        description="An activity is something that occurs over a period of time and acts upon or with entities; "
                    "it may include consuming, processing, transforming, modifying, relocating, using, or generating "
                    "entities.",
        rdf_term=PROV.hadActivity,
        rdf_type="uri"
    )


class End(InstantaneousEvent, EntityInfluence):
    model_config = ConfigDict(title=PROV.End)


class Start(InstantaneousEvent, EntityInfluence):
    model_config = ConfigDict(title=PROV.Start)


class Activity(RDFModel):
    model_config = ConfigDict(title=PROV.Activity)

    generated: List[Union[AnyHttpUrl, RDFModel]] = Field(
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
    wasAssociatedWith: Union[AnyHttpUrl, RDFModel] = Field(
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
    wasEndedBy: AnyHttpUrl = Field(
        default=None,
        description="End is when an activity is deemed to have been ended by an entity, known as trigger. "
                    "The activity no longer exists after its end. Any usage, generation, or invalidation involving an "
                    "activity precedes the activity's end. An end may refer to a trigger entity that terminated "
                    "the activity, or to an activity, known as ender that generated the trigger.",
        rdf_term=PROV.wasEndedBy,
        rdf_type="uri"
    )
    qualifiedUsage: List[Union[AnyHttpUrl, RDFModel]] = Field(
        default=None,
        description="Usage is the beginning of utilizing an entity by an activity. "
                    "Before usage, the activity had not begun to utilize this entity and could not have been affected "
                    "by the entity.",
        rdf_term=PROV.qualifiedUsage,
        rdf_type="uri"
    )
    used: AnyHttpUrl = Field(
        default=None,
        description="Usage is the beginning of utilizing an entity by an activity. Before usage, the activity had not "
                    "begun to utilize this entity and could not have been affected by the entity.", 
        rdf_term=PROV.used,
        rdf_type="uri"
    )
    invalidated: List[Union[AnyHttpUrl, RDFModel]] = Field(
        default=None,
        description="Invalidation is the start of the destruction, cessation, or expiry of an existing entity by "
                    "an activity. The entity is no longer available for use (or further invalidation) after "
                    "invalidation. Any generation or usage of an entity precedes its invalidation.",
        rdf_term=PROV.invalidated,
        rdf_type="uri"
    )
    endedAtTime: Union[AwareDatetime, NaiveDatetime] = Field(
        default=None,
        description="End is when an activity is deemed to have been ended by an entity, known as trigger. "
                    "The activity no longer exists after its end. Any usage, generation, or invalidation "
                    "involving an activity precedes the activity's end. An end may refer to a trigger entity that "
                    "terminated the activity, or to an activity, known as ender that generated the trigger.", 
        rdf_term=PROV.endedAtTime,
        rdf_type="xsd:dateTime"
    )
    qualifiedStart: Start = Field(
        default=None,
        description="Start is when an activity is deemed to have been started by an entity, known as trigger. "
                    "The activity did not exist before its start. Any usage, generation, or invalidation involving "
                    "an activity follows the activity's start. A start may refer to a trigger entity that set off "
                    "the activity, or to an activity, known as starter, that generated the trigger.", 
        rdf_term=PROV.qualifiedStart,
        rdf_type=Start
    )
    wasInformedBy: List[Union[AnyHttpUrl, RDFModel]] = Field(
        default=None,
        description="Communication is the exchange of an entity by two activities, one activity using the entity "
                    "generated by the other.",
        rdf_term=PROV.wasInformedBy,
        rdf_type="uri"
    )
    wasStartedBy: Union[AnyHttpUrl, RDFModel] = Field(
        default=None,
        description="Start is when an activity is deemed to have been started by an entity, known as trigger. "
                    "The activity did not exist before its start. Any usage, generation, or invalidation involving an "
                    "activity follows the activity's start. A start may refer to a trigger entity that set off "
                    "the activity, or to an activity, known as starter, that generated the trigger.", 
        rdf_term=PROV.wasStartedBy,
        rdf_type="uri"
    )
    startedAtTime: Union[AwareDatetime, NaiveDatetime] = Field(
        default=None,
        description="Start is when an activity is deemed to have been started by an entity, known as trigger. "
                    "The activity did not exist before its start. Any usage, generation, or invalidation involving an "
                    "activity follows the activity's start. A start may refer to a trigger entity that set off"
                    " the activity, or to an activity, known as starter, that generated the trigger.", 
        rdf_term=PROV.startedAtTime,
        rdf_type="xsd:dateTime"
    )
    qualifiedCommunication: List[Union[AnyHttpUrl, RDFModel]] = Field(
        default=None,
        description="Communication is the exchange of an entity by two activities, one activity using the entity "
                    "generated by the other.",
        rdf_term=PROV.qualifiedCommunication,
        rdf_type="uri"
    )
    wasInfluencedBy: List[Union[AnyHttpUrl, RDFModel]] = Field(
        default=None,
        description="Influence is the capacity of an entity, activity, or agent to have an effect on the character, "
                    "development, or behavior of another by means of usage, start, end, generation, invalidation, "
                    "communication, derivation, attribution, association, or delegation.", 
        rdf_term=PROV.wasInfluencedBy,
        rdf_type="uri"
    )
    qualifiedInfluence: List[Union[AnyHttpUrl, RDFModel]] = Field(
        default=None,
        description="Influence is the capacity of an entity, activity, or agent to have an effect on the character, "
                    "development, or behavior of another by means of usage, start, end, generation, invalidation, "
                    "communication, derivation, attribution, association, or delegation.", 
        rdf_term=PROV.qualifiedInfluence,
        rdf_type="uri"
    )
    atLocation: Union[AnyHttpUrl, RDFModel] = Field(
        default=None,
        description="A location can be an identifiable geographic place (ISO 19112), but it can also be a "
                    "non-geographic place such as a directory, row, or column. As such, there are numerous ways in "
                    "which location can be expressed, such as by a coordinate, address, landmark, and so forth.",
        rdf_term=PROV.atLocation,
        rdf_type="uri"
    )
