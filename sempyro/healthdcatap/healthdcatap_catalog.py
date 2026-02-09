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

from pydantic import ConfigDict
from rdflib.namespace import DCAT

from sempyro.dcat import DCATCatalog


class HEALTHDCATAPCatalog(DCATCatalog):
    model_config = ConfigDict(
        json_schema_extra={
            "$ontology": [
                "https://www.w3.org/TR/vocab-dcat-3/",
                "https://healthdataeu.pages.code.europa.eu/healthdcat-ap/releases/release-6/",
            ],
            "$namespace": str(DCAT),
            "$IRI": DCAT.Catalog,
            "$prefix": "dcat",
        }
    )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "health_dcat")
    HEALTHDCATAPCatalog.save_schema_to_file(Path(json_models_folder, "HEALTHDCATAPCatalog.json"), "json")
    HEALTHDCATAPCatalog.save_schema_to_file(Path(json_models_folder, "HEALTHDCATAPCatalog.yaml"), "yaml")
