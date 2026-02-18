# Copyright 2026 Stichting Health-RI
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
from typing import Union, List

from pydantic import AnyHttpUrl, ConfigDict, Field
from rdflib.namespace import DCAT

from sempyro.dcat import DCATDistribution
from sempyro.namespaces import HEALTHDCATAP, DCATAPv3
from sempyro.time import PeriodOfTime


class HEALTHDCATAPDistribution(DCATDistribution):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": [
                "https://www.w3.org/TR/vocab-dcat-3/",
                "https://healthdataeu.pages.code.europa.eu/healthdcat-ap/releases/release-6/",
            ],
            "$namespace": str(DCAT),
            "$IRI": DCAT.Distribution,
            "$prefix": "dcat",
        },
    )
    retention_period: Union[AnyHttpUrl, PeriodOfTime] = Field(
        default=None,
        description="A temporal period which the dataset is available for secondary use.",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.retentionPeriod,
            "rdf_type": "uri",
        },
    )
    applicable_legislation: List[AnyHttpUrl] = Field(
        description="The legislation that is applicable to this resource.",
        json_schema_extra={
            "rdf_term": DCATAPv3.applicableLegislation,
            "rdf_type": "uri",
        },
    )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "health_dcat")
    HEALTHDCATAPDistribution.save_schema_to_file(Path(json_models_folder, "HEALTHDCATAPDistribution.json"), "json")
    HEALTHDCATAPDistribution.save_schema_to_file(Path(json_models_folder, "HEALTHDCATAPDistribution.yaml"), "yaml")
