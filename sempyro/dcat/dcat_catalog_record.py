# Copyright 2025 Stichting Health-RI
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

from datetime import date
from typing import Union

from pydantic import ConfigDict, AwareDatetime, NaiveDatetime, Field, field_validator, AnyHttpUrl
from rdflib import DCAT, DCTERMS, FOAF

from sempyro import RDFModel
from sempyro.utils.validator_functions import date_handler


class DCATCatalogRecord(RDFModel):
    """A description of a Catalogued Resource's entry in the Catalogue. """
    model_config = ConfigDict(json_schema_extra={
                                  "$ontology": "https://www.w3.org/TR/vocab-dcat-3/",
                                  "$namespace": str(DCAT),
                                  "$IRI": DCAT.CatalogRecord,
                                  "$prefix": "dcat"
                              })
    modification_date: Union[str, date, AwareDatetime, NaiveDatetime] = Field(
        description="The most recent date on which the Catalogue entry was changed or modified. ",
        json_schema_extra={
            "rdf_term": DCTERMS.modified,
            "rdf_type": "datetime_literal"
        }
    )

    primary_topic: AnyHttpUrl = Field(
        description="A link to the Dataset, Data service or Catalog described in the record. ",
        json_schema_extra={
            "rdf_term": FOAF.primaryTopic,
            "rdf_type": "uri"
        }
    )

    @field_validator("modification_date", mode="before")
    @classmethod
    def date_validator(cls, value):
        return date_handler(value)
