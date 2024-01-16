from abc import ABCMeta, ABC
from pydantic import BaseModel, Field, ConfigDict

# $schema: https://json-schema.org/draft/2020-12/schema
# title: Ontology Term
# description: Definition of an ontology term.


class BeaconOntologyTerm(BaseModel, metaclass=ABCMeta):
    model_config = ConfigDict(extra="allow")
    id: str = Field(description="Definition of an identifier in the CURIE `prefix:local-part` format which is the "
                                "default type of e.g. ontology term `id` values (used e.g. for filters or "
                                "external identifiers).",
                    pattern=r"^\w[^:]+:.+$",
                    examples=["ga4gh:GA.01234abcde", "DUO:0000004", "orcid:0000-0003-3463-0775", "PMID:15254584"]
                    )
    label: str = Field(default=None,
                       description="The text that describes the term. By default it could be the preferred text of "
                                   "the term, but is it acceptable to customize it for a clearer description and "
                                   "understanding of the term in an specific context.")
