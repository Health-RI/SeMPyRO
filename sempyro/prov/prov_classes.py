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

from pydantic import AnyHttpUrl, AwareDatetime, ConfigDict, Field, NaiveDatetime
from rdflib import PROV

from sempyro import RDFModel


class Association(RDFModel):
    """
    An activity association is an assignment of responsibility to an agent for an activity, indicating that the agent
    had a role in the activity. It further allows for a plan to be specified, which is the plan intended by the agent
    to achieve some goals in the context of this activity.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "$ontology": "https://www.w3.org/TR/prov-o/",
            "$namespace": str(PROV),
            "$IRI": PROV.Association,
            "$prefix": "prov"
        }
    )

    hadPlan: AnyHttpUrl = Field(
        default=None,
        description="A plan is an entity that represents a set of actions or steps intended by one or more agents to "
                    "achieve some goals.",
        json_schema_extra={
            "rdf_term": PROV.hadPlan,
            "rdf_type": "uri"
        }
    )
    hadRole: AnyHttpUrl = Field(
        default=None,
        description="A role is the function of an entity or agent with respect to an activity, in the context of "
                    "a usage, generation, invalidation, association, start, and end.",
        json_schema_extra={
            "rdf_term": PROV.hadRole,
            "rdf_type": "uri"
        }
    )
    agent: AnyHttpUrl = Field(
        default=None,
        description="The prov:agent property references an prov:Agent which influenced a resource. "
                    "This property applies to an prov:AgentInfluence, which is given by a subproperty of "
                    "prov:qualifiedInfluence from the influenced prov:Entity, prov:Activity or prov:Agent.",
        json_schema_extra={
            "rdf_term": PROV.Agent,
            "rdf_type": "uri"
        }
    )


class InstantaneousEvent(RDFModel):
    """
    The PROV data model is implicitly based on a notion of instantaneous events (or just events), that mark
    transitions in the world. Events include generation, usage, or invalidation of entities, as well as starting or
    ending of activities. This notion of event is not first-class in the data model, but it is useful for explaining
    its other concepts and its semantics.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "$ontology": "https://www.w3.org/TR/prov-o/",
            "$namespace": str(PROV),
            "$IRI": PROV.InstantaneousEvent,
            "$prefix": "prov"
        }
    )

    atTime: Union[NaiveDatetime, AwareDatetime] = Field(
        default=None,
        description="The PROV data model is implicitly based on a notion of instantaneous events (or just events), "
                    "that mark transitions in the world. Events include generation, usage, or invalidation of entities,"
                    " as well as starting or ending of activities. This notion of event is not first-class in the data "
                    "model, but it is useful for explaining its other concepts and its semantics.",
        json_schema_extra={
            "rdf_term": PROV.InstantaneousEvent,
            "rdf_type": "xsd:dateTime"
        }
    )
    hadRole: AnyHttpUrl = Field(
        default=None,
        description="A role is the function of an entity or agent with respect to an activity, in the context of "
                    "a usage, generation, invalidation, association, start, and end.",
        json_schema_extra={
            "rdf_term": PROV.hadRole,
            "rdf_type": "uri"
        }
    )
    atLocation: AnyHttpUrl = Field(
        default=None,
        description="A location can be an identifiable geographic place (ISO 19112), but it can also be a "
                    "non-geographic place such as a directory, row, or column. As such, there are numerous ways in "
                    "which location can be expressed, such as by a coordinate, address, landmark, and so forth.",
        json_schema_extra={
            "rdf_term": PROV.atLocation,
            "rdf_type": "uri"
        }
    )


class EntityInfluence(RDFModel):
    """
    EntityInfluence is the capacity of an entity to have an effect on the character, development, or behavior of 
    another by means of usage, start, end, derivation, or other.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "$ontology": "https://www.w3.org/TR/prov-o/",
            "$namespace": str(PROV),
            "$IRI": PROV.EntityInfluence,
            "$prefix": "prov"
        }
    )

    entity: AnyHttpUrl = Field(
        default=None,
        description="The prov:entity property references an prov:Entity which influenced a resource. This property "
                    "applies to an prov:EntityInfluence, which is given by a subproperty of prov:qualifiedInfluence "
                    "from the influenced prov:Entity, prov:Activity or prov:Agent.",
        json_schema_extra={
            "rdf_term": PROV.Entity,
            "rdf_type": "uri"
        }
    )
    hadRole: AnyHttpUrl = Field(
        default=None,
        description="A role is the function of an entity or agent with respect to an activity, in the context of "
                    "a usage, generation, invalidation, association, start, and end.",
        json_schema_extra={
            "rdf_term": PROV.hadRole,
            "rdf_type": "uri"
        }
    )
    influencer: AnyHttpUrl = Field(
        default=None,
        description="This property is used as part of the qualified influence pattern. Subclasses of prov:Influence "
                    "use these subproperties to reference the resource (Entity, Agent, or Activity) whose influence is "
                    "being qualified.",
        json_schema_extra={
            "rdf_term": PROV.influencer,
            "rdf_type": "uri"
        }
    )
    hadActivity: AnyHttpUrl = Field(
        default=None,
        description="An activity is something that occurs over a period of time and acts upon or with entities; "
                    "it may include consuming, processing, transforming, modifying, relocating, using, or generating "
                    "entities.",
        json_schema_extra={
            "rdf_term": PROV.hadActivity,
            "rdf_type": "uri"
        }
    )


class End(InstantaneousEvent, EntityInfluence):
    """
    End is when an activity is deemed to have been ended by an entity, known as trigger. The activity no longer exists
    after its end. Any usage, generation, or invalidation involving an activity precedes the activity's end.
    An end may refer to a trigger entity that terminated the activity, or to an activity, known as ender that generated
    the trigger.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "$ontology": "https://www.w3.org/TR/prov-o/",
            "$namespace": str(PROV),
            "$IRI": PROV.End,
            "$prefix": "prov"
        })


class Start(InstantaneousEvent, EntityInfluence):
    """
    Start is when an activity is deemed to have been started by an entity, known as trigger. The activity did
    not exist before its start. Any usage, generation, or invalidation involving an activity follows the
    activity's start. A start may refer to a trigger entity that set off the activity, or to an activity, known as
    starter, that generated the trigger.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "$ontology": "https://www.w3.org/TR/prov-o/",
            "$namespace": str(PROV),
            "$IRI": PROV.Start,
            "$prefix": "prov"
        }
    )


class Activity(RDFModel):
    """
    An activity is something that occurs over a period of time and acts upon or with entities; it may include 
    consuming, processing, transforming, modifying, relocating, using, or generating entities.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "$ontology": "https://www.w3.org/TR/prov-o/",
            "$namespace": str(PROV),
            "$IRI": PROV.Activity,
            "$prefix": "prov"
        }
    )

    generated: List[AnyHttpUrl] = Field(
        default=None,
        description="Generation is the completion of production of a new entity by an activity. This entity did not "
                    "exist before generation and becomes available for usage after this generation.",
        json_schema_extra={
            "rdf_term": PROV.generated,
            "rdf_type": "uri"
        }
    )
    qualifiedAssociation: List[Union[AnyHttpUrl, Association]] = Field(
        default=None,
        description="An activity association is an assignment of responsibility to an agent for an activity, "
                    "indicating that the agent had a role in the activity. It further allows for a plan to be "
                    "specified, which is the plan intended by the agent to achieve some goals in the context of this "
                    "activity.",
        json_schema_extra={
            "rdf_term": PROV.qualifiedQuotation,
            "rdf_type": "uri"
        }
    )
    wasAssociatedWith: AnyHttpUrl = Field(
        default=None,
        description="An activity association is an assignment of responsibility to an agent for an activity, "
                    "indicating that the agent had a role in the activity. It further allows for a plan to be "
                    "specified, which is the plan intended by the agent to achieve some goals in the context of this "
                    "activity.",
        json_schema_extra={
            "rdf_term": PROV.wasAssociatedWith,
            "rdf_type": "uri"
        }
    )
    qualifiedEnd: End = Field(
        default=None,
        description="End is when an activity is deemed to have been ended by an entity, known as trigger. "
                    "The activity no longer exists after its end. Any usage, generation, or invalidation involving "
                    "an activity precedes the activity's end. An end may refer to a trigger entity that terminated "
                    "the activity, or to an activity, known as ender that generated the trigger.",
        json_schema_extra={
            "rdf_term": PROV.qualifiedEnd,
            "rdf_type": PROV.End
        }
    )
    wasEndedBy: AnyHttpUrl = Field(
        default=None,
        description="End is when an activity is deemed to have been ended by an entity, known as trigger. "
                    "The activity no longer exists after its end. Any usage, generation, or invalidation involving an "
                    "activity precedes the activity's end. An end may refer to a trigger entity that terminated "
                    "the activity, or to an activity, known as ender that generated the trigger.",
        json_schema_extra={
            "rdf_term": PROV.wasEndedBy,
            "rdf_type": "uri"
        }
    )
    qualifiedUsage: List[AnyHttpUrl] = Field(
        default=None,
        description="Usage is the beginning of utilizing an entity by an activity. "
                    "Before usage, the activity had not begun to utilize this entity and could not have been affected "
                    "by the entity.",
        json_schema_extra={
            "rdf_term": PROV.qualifiedUsage,
            "rdf_type": "uri"
        }
    )
    used: AnyHttpUrl = Field(
        default=None,
        description="Usage is the beginning of utilizing an entity by an activity. Before usage, the activity had not "
                    "begun to utilize this entity and could not have been affected by the entity.",
        json_schema_extra={
            "rdf_term": PROV.used,
            "rdf_type": "uri"
        }
    )
    invalidated: List[AnyHttpUrl] = Field(
        default=None,
        description="Invalidation is the start of the destruction, cessation, or expiry of an existing entity by "
                    "an activity. The entity is no longer available for use (or further invalidation) after "
                    "invalidation. Any generation or usage of an entity precedes its invalidation.",
        json_schema_extra={
            "rdf_term": PROV.invalidated,
            "rdf_type": "uri"
        }
    )
    endedAtTime: Union[AwareDatetime, NaiveDatetime] = Field(
        default=None,
        description="End is when an activity is deemed to have been ended by an entity, known as trigger. "
                    "The activity no longer exists after its end. Any usage, generation, or invalidation "
                    "involving an activity precedes the activity's end. An end may refer to a trigger entity that "
                    "terminated the activity, or to an activity, known as ender that generated the trigger.",
        json_schema_extra={
            "rdf_term": PROV.endedAtTime,
            "rdf_type": "xsd:dateTime"
        }
    )
    qualifiedStart: Start = Field(
        default=None,
        description="Start is when an activity is deemed to have been started by an entity, known as trigger. "
                    "The activity did not exist before its start. Any usage, generation, or invalidation involving "
                    "an activity follows the activity's start. A start may refer to a trigger entity that set off "
                    "the activity, or to an activity, known as starter, that generated the trigger.",
        json_schema_extra={
            "rdf_term": PROV.qualifiedStart,
            "rdf_type": PROV.Start
        }
    )
    wasInformedBy: List[AnyHttpUrl] = Field(
        default=None,
        description="Communication is the exchange of an entity by two activities, one activity using the entity "
                    "generated by the other.",
        json_schema_extra={
            "rdf_term": PROV.wasInformedBy,
            "rdf_type": "uri"
        }
    )
    wasStartedBy: AnyHttpUrl = Field(
        default=None,
        description="Start is when an activity is deemed to have been started by an entity, known as trigger. "
                    "The activity did not exist before its start. Any usage, generation, or invalidation involving an "
                    "activity follows the activity's start. A start may refer to a trigger entity that set off "
                    "the activity, or to an activity, known as starter, that generated the trigger.",
        json_schema_extra={
            "rdf_term": PROV.wasStartedBy,
            "rdf_type": "uri"
        }
    )
    startedAtTime: Union[AwareDatetime, NaiveDatetime] = Field(
        default=None,
        description="Start is when an activity is deemed to have been started by an entity, known as trigger. "
                    "The activity did not exist before its start. Any usage, generation, or invalidation involving an "
                    "activity follows the activity's start. A start may refer to a trigger entity that set off"
                    " the activity, or to an activity, known as starter, that generated the trigger.",
        json_schema_extra={
            "rdf_term": PROV.startedAtTime,
            "rdf_type": "xsd:dateTime"
        }
    )
    qualifiedCommunication: List[AnyHttpUrl] = Field(
        default=None,
        description="Communication is the exchange of an entity by two activities, one activity using the entity "
                    "generated by the other.",
        json_schema_extra={
            "rdf_term": PROV.qualifiedCommunication,
            "rdf_type": "uri"
        }
    )
    wasInfluencedBy: List[AnyHttpUrl] = Field(
        default=None,
        description="Influence is the capacity of an entity, activity, or agent to have an effect on the character, "
                    "development, or behavior of another by means of usage, start, end, generation, invalidation, "
                    "communication, derivation, attribution, association, or delegation.",
        json_schema_extra={
            "rdf_term": PROV.wasInfluencedBy,
            "rdf_type": "uri"
        }
    )
    qualifiedInfluence: List[AnyHttpUrl] = Field(
        default=None,
        description="Influence is the capacity of an entity, activity, or agent to have an effect on the character, "
                    "development, or behavior of another by means of usage, start, end, generation, invalidation, "
                    "communication, derivation, attribution, association, or delegation.",
        json_schema_extra={
            "rdf_term": PROV.qualifiedInfluence,
            "rdf_type": "uri"
        }
    )
    atLocation: AnyHttpUrl = Field(
        default=None,
        description="A location can be an identifiable geographic place (ISO 19112), but it can also be a "
                    "non-geographic place such as a directory, row, or column. As such, there are numerous ways in "
                    "which location can be expressed, such as by a coordinate, address, landmark, and so forth.",
        json_schema_extra={
            "rdf_term": PROV.atLocation,
            "rdf_type": "uri"
        }
    )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "prov")
    models = ["Association", "Activity", "Start", "End", "EntityInfluence", "InstantaneousEvent"]
    for model_name in models:
        model = globals()[model_name]
        model.save_schema_to_file(path=Path(json_models_folder, f"{model_name}.json"),
                                  file_format="json")
        model.save_schema_to_file(path=Path(json_models_folder, f"{model_name}.yaml"),
                                  file_format="yaml")
