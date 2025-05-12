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

from pydantic import AnyHttpUrl, ConfigDict, Field, field_validator
from rdflib.namespace import DCAT, DCTERMS

from sempyro import LiteralField
from sempyro.dcat import DCATDistribution
from sempyro.hri_dcat import HRIDataService
from sempyro.hri_dcat.vocabularies import GeonovumLicences
from sempyro.utils.validator_functions import force_literal_field


class HRIDistribution(DCATDistribution):
    """
    A specific representation of a dataset. A dataset might be available in multiple serializations that may differ
    in various ways, including natural language, media-type or format, schematic organization, temporal and spatial
    resolution, level of detail or profiles (which might specify any or all of the above).
    """
    model_config = ConfigDict(arbitrary_types_allowed=True,
                              use_enum_values=True,
                              json_schema_extra={
                                  "$ontology": ["https://www.w3.org/TR/vocab-dcat-3/",
                                                "https://health-ri.atlassian.net/wiki/spaces/FSD/pages/121110529/"
                                                "Core+Metadata+Schema+Specification"],
                                  "$namespace": str(DCAT),
                                  "$IRI": DCAT.Distribution,
                                  "$prefix": "dcat"
                              }
                              )

    title: List[LiteralField] = Field(
        default=None,
        description="A name given to the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.title,
            "rdf_type": "rdfs_literal"
        }
    )
    description: List[LiteralField] = Field(
        default=None,
        description="An account of the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.description,
            "rdf_type": "rdfs_literal"
        }
    )
    access_url: AnyHttpUrl = Field(
        description="A URL of the resource that gives access to a distribution of the dataset. E.g., landing page, "
                    "feed, SPARQL endpoint.",
        json_schema_extra={
            "rdf_term": DCAT.accessURL,
            "rdf_type": "uri"
        }
    )
    media_type: AnyHttpUrl = Field(
        default=None,
        description="The media type of the distribution as defined by IANA.",
        json_schema_extra={
            "rdf_term": DCAT.mediaType,
            "rdf_type": "uri"
        }
    )
    format: AnyHttpUrl = Field(
        description="The file format, physical medium, or dimensions of the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.format,
            "rdf_type": "uri"
        }
    )
    license: Union[AnyHttpUrl, GeonovumLicences] = Field(
        description="A legal document giving official permission to do something with the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.license,
            "rdf_type": "uri"
        }
    )
    access_service: Union[AnyHttpUrl, HRIDataService] = Field(
        default=None,
        description="A data service that gives access to the distribution of the dataset.",
        json_schema_extra={
            "rdf_term": DCAT.accessService,
            "rdf_type": "uri"
        }
    )
    download_url: AnyHttpUrl = Field(
        default=None,
        description="The URL of the downloadable file in a given format. E.g., CSV file or RDF file. "
                    "The format is indicated by the distribution's dcterms:format and/or dcat:mediaType.",
        json_schema_extra={
            "rdf_term": DCAT.downloadURL,
            "rdf_type": "uri"
        }
    )
    rights: AnyHttpUrl = Field(
        description="Information about rights held in and over the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.rights,
            "rdf_type": "uri"
        }
    )
    byte_size: Union[int, LiteralField] = Field(
        description="The size of a distribution in bytes.",
        json_schema_extra={
            "rdf_term": DCAT.byteSize,
            "rdf_type": "xsd:integer"
        }
    )

    @field_validator("title", "description", mode="before")
    @classmethod
    def convert_to_literal(cls, value: List[Union[str, LiteralField]]) -> List[LiteralField]:
        if not value:
            return None
        return [force_literal_field(item) for item in value]


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "hri_dcat")
    HRIDistribution.save_schema_to_file(Path(json_models_folder, "HRIDistribution.json"), "json")
    HRIDistribution.save_schema_to_file(Path(json_models_folder, "HRIDistribution.yaml"), "yaml")
