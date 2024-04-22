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
from typing import List, Union

from pydantic import AnyHttpUrl, ConfigDict, Field
from rdflib.namespace import DCAT, DCTERMS, PROV

from sempyro import LiteralField
from sempyro.dcat import DCATResource
from sempyro.geo import Location
from sempyro.namespaces import FREQ, DCATv3
from sempyro.prov import Activity
from sempyro.time import PeriodOfTime


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
        rdf_term=DCAT.distribution,
        rdf_type="uri"
    )
    temporal_coverage: List[PeriodOfTime] = Field(
        default=None,
        description="The temporal period that the dataset covers.",
        rdf_term=DCTERMS.temporal,
        rdf_type=DCTERMS.PeriodOfTime
    )
    frequency: Union[AnyHttpUrl, Frequency] = Field(
        default=None,
        description="The frequency at which a dataset is published.",
        rfd_term=DCTERMS.accrualPeriodicity,
        rdf_type="uri"
    )
    in_series: List[AnyHttpUrl] = Field(
        default=None,
        description="A dataset series of which the dataset is part.",
        rdf_term=DCATv3.inSeries,
        rdf_type="uri"
    )
    spatial: List[Union[AnyHttpUrl, Location]] = Field(
        default=None,
        description="The geographical area covered by the dataset.",
        rdf_term=DCTERMS.spatial,
        rdf_type="uri")

    spatial_resolution: List[float] = Field(
        default=None,
        description="Minimum spatial separation resolvable in a dataset, "
                    "measured in meters.",
        rdf_term=DCAT.spatialResolutionInMeters,
        rdf_type="xsd:decimal")

    temporal_resolution: List[Union[str, LiteralField]] = Field(
        default=None,
        description="Minimum time period resolvable in the dataset.",
        rdf_term=DCAT.temporalResolution,
        rdf_type="xsd:duration"
    )

    was_generated_by: List[Union[AnyHttpUrl, Activity]] = Field(
        default=None,
        description="An activity that generated, or provides the business context for, the creation of the dataset.",
        rdf_term=PROV.wasGeneratedBy,
        rdf_type="uri"
    )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "dcat")
    DCATDataset.save_schema_to_file(Path(json_models_folder, "DCATDataset.json"), "json")
    DCATDataset.save_schema_to_file(Path(json_models_folder, "DCATDataset.yaml"), "yaml")
