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

from enum import Enum
from pathlib import Path
from typing import List, Union, Optional

from pydantic import AnyHttpUrl, ConfigDict, Field, field_validator
from rdflib.namespace import DCAT, DCTERMS, PROV

from sempyro import LiteralField
from sempyro.dcat import DCATResource
from sempyro.namespaces import FREQ, DCATv3
from sempyro.prov import Activity


class Frequency(Enum):
    triennial = FREQ.triennial
    biennial = FREQ.biennial
    annual = FREQ.annual
    semiannual = FREQ.semiannual
    threeTimesAYear = FREQ.threeTimesAYear
    quarterly = FREQ.quarterly
    bimonthly = FREQ.bimonthly
    monthly = FREQ.monthly
    semimonthly = FREQ.semimonthly
    biweekly = FREQ.biweekly
    threeTimesAMonth = FREQ.threeTimesAMonth
    weekly = FREQ.weekly
    semiweekly = FREQ.semiweekly
    threeTimesAWeek = FREQ.threeTimesAWeek
    daily = FREQ.daily
    continuous = FREQ.continuous
    irregular = FREQ.irregular


class DCATDataset(DCATResource):
    model_config = ConfigDict(
                              json_schema_extra={
                                  "$ontology": "https://www.w3.org/TR/vocab-dcat-3/",
                                  "$namespace": str(DCAT),
                                  "$IRI": DCAT.Dataset,
                                  "$prefix": "dcat"
                              }
                              )

    distribution: List[AnyHttpUrl] = Field(
        default=None,
        description="An available distribution of the dataset.",
        json_schema_extra={
            "rdf_term": DCAT.distribution,
            "rdf_type": "uri"
        }
    )
    frequency: Union[AnyHttpUrl, Frequency] = Field(
        default=None,
        description="The frequency at which a dataset is published.",
        json_schema_extra={
            "rdf_term": DCTERMS.accrualPeriodicity,
            "rdf_type": "uri"
        }
    )
    in_series: List[AnyHttpUrl] = Field(
        default=None,
        description="A dataset series of which the dataset is part.",
        json_schema_extra={
            "rdf_term": DCATv3.inSeries,
            "rdf_type": "uri"
        }
    )
    spatial_resolution: List[float] = Field(
        default=None,
        description="Minimum spatial separation resolvable in a dataset, "
                    "measured in meters.",
        json_schema_extra={
            "rdf_term": DCAT.spatialResolutionInMeters,
            "rdf_type": "xsd:decimal"
        }
    )
    temporal_resolution: Union[str, LiteralField] = Field(
        default=None,
        description="Minimum time period resolvable in the dataset.",
        json_schema_extra={
            "rdf_term": DCAT.temporalResolution,
            "rdf_type": "xsd:duration"
        }
    )
    was_generated_by: List[Union[AnyHttpUrl, Activity]] = Field(
        default=None,
        description="An activity that generated, or provides the business context for, the creation of the dataset.",
        json_schema_extra={
            "rdf_term": PROV.wasGeneratedBy,
            "rdf_type": "uri"
        }
    )
    access_rights: Optional[AnyHttpUrl] = Field(
        default=None,
        description="Information about who can access the dataset and under what conditions.",
        json_schema_extra={
            "rdf_term": DCTERMS.accessRights,
            "rdf_type": "uri"
        }
    )

    @field_validator("temporal_resolution", mode="after")
    @classmethod
    def validate_xsd_duration(cls, value: Union[str, LiteralField]) -> LiteralField:
        if isinstance(value, str):
            return LiteralField(value=value, datatype="xsd:duration")
        if isinstance(value, LiteralField) and value.datatype != "xsd:duration":
            return LiteralField(value=value.value, datatype="xsd:duration")
        return value


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "dcat")
    DCATDataset.save_schema_to_file(Path(json_models_folder, "DCATDataset.json"), "json")
    DCATDataset.save_schema_to_file(Path(json_models_folder, "DCATDataset.yaml"), "yaml")
