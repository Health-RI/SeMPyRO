import json
import logging
import re
from pathlib import Path
from pydantic import ConfigDict, Field, AnyHttpUrl, AnyUrl, field_validator
from typing import List, Union
from rdflib import Namespace, URIRef
from rdflib.namespace import DCTERMS, FOAF
from pydantic.networks import validate_email

from dcat.rdf_model import RDFModel, LiteralField

logger = logging.getLogger("__name__")

VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")


class VCard(RDFModel):
    """
    The vCard class is equivalent to the new Kind class, which is the parent for the four explicit types
    of vCards (Individual, Organization, Location, Group)
    """
    model_config = ConfigDict(
        title=VCARD.VCard,
                              json_schema_extra={
                                  "$ontology": "https://www.w3.org/TR/vcard-rdf/",
                                  "$namespace": VCARD,
                                  "$IRI": VCARD.VCard,
                                  "$prefix": "v"
                              }
                              )

    hasEmail: List[AnyUrl] = Field(default=None,
                                   description="The email address as a mailto URI",
                                   rdf_term=VCARD.hasEmail,
                                   rdf_type="uri"
                                   )
    full_name: List[Union[str, LiteralField]] = Field(default=None,
                                                      description="The full name of the object (as a single string). "
                                                                  "This is the only mandatory property.",
                                                      rdf_term=VCARD.fn,
                                                      rdf_type="rdfs_literal"
                                                      )
    hasUID: AnyHttpUrl = Field(description="A unique identifier for the object",
                               rdf_term=VCARD.hasUID,
                               rdf_type="uri"
                               )

    @classmethod
    def _convert_to_mailto(cls, value: str) -> AnyUrl:
        mail_part = value
        if value.startswith("mailto:"):
            mail_part = re.split(":|\//", value)[-1]
        mail_part = validate_email(mail_part)[1]
        return AnyUrl(f"mailto:{mail_part}")

    @field_validator("hasEmail", mode="before")
    @classmethod
    def _validate_email(cls, value: Union[str, AnyUrl]) -> List[AnyUrl]:
        """
        Checks if provided value is a valid email or mailto URI, fulfills an email to mailto URI
        """
        if not isinstance(value, list):
            value = [value]
        new_list = [cls._convert_to_mailto(item) for item in value]
        return new_list


class Agent(RDFModel):
    model_config = ConfigDict(title=FOAF.Agent)

    name: List[Union[str, LiteralField]] = Field(description="A name of the agent",
                                                 rdf_term=FOAF.name,
                                                 rdf_type="rdfs_literal"
                                                 )
    identifier: Union[str, LiteralField] = Field(description="A unique identifier of the agent.",
                                                 rdf_term=DCTERMS.identifier,
                                                 rdf_type="rdfs_literal")


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parent.resolve(), "json_models")
    models = ["VCard", "Agent"]
    for model_name in models:
        with open(Path(json_models_folder, f"{model_name}.json"), "w") as schema_file:
            model_schema = globals()[model_name].model_json_schema()
            json.dump(model_schema, schema_file, indent=2)
