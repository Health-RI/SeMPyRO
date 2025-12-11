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

from datetime import datetime
from pathlib import Path
from typing import Union

from pydantic import ConfigDict, Field, field_validator
from rdflib import DCAT, DCTERMS, Namespace

from sempyro.rdf_model import RDFModel

VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")


class HRIPeriodOfTime(RDFModel):
    model_config = ConfigDict(
        json_schema_extra={
            "$ontology": "https://www.w3.org/TR/vocab-dcat-3/#Class:Period_of_Time",
            "$namespace": str(DCTERMS),
            "$IRI": DCTERMS.PeriodOfTime,
            "$prefix": "dcterms",
        }
    )
    """
    An interval of time that is named or defined by its start and end,
    https://www.w3.org/TR/vocab-dcat-3/#Class:Period_of_Time
    """
    start_date: datetime = Field(
        default=None,
        description="The start of the period",
        json_schema_extra={
            "rdf_term": DCAT.startDate,
            "rdf_type": "xsd:dateTime",
        },
    )
    end_date: datetime = Field(
        default=None,
        description="The end of the period",
        json_schema_extra={
            "rdf_term": DCAT.endDate,
            "rdf_type": "xsd:dateTime",
        },
    )

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def convert_to_datetime(cls, value: Union[str, datetime]) -> datetime:
        return datetime.fromisoformat(value) if isinstance(value, str) else value


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "hri_dcat")
    HRIPeriodOfTime.save_schema_to_file(path=Path(json_models_folder, "HRIPeriodOfTime.json"), file_format="json")
    HRIPeriodOfTime.save_schema_to_file(path=Path(json_models_folder, "HRIPeriodOfTime.yaml"), file_format="yaml")
