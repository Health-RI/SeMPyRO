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

from datetime import date, datetime
from pathlib import Path
from pydantic import Field, AnyHttpUrl, ConfigDict, AwareDatetime, NaiveDatetime, field_validator
from rdflib.namespace import DCAT, DCTERMS, ODRL2
from typing import List, Union

from sempyro import RDFModel, LiteralField
from sempyro.dcat import DataService
from sempyro.odrl import ODRLPolicy
from sempyro.spdx import SPDX, Checksum
from sempyro.utils.validator_functions import force_literal_field


class DCATDistribution(RDFModel):
    """
    A specific representation of a dataset. A dataset might be available in multiple serializations that may differ
    in various ways, including natural language, media-type or format, schematic organization, temporal and spatial
    resolution, level of detail or profiles (which might specify any or all of the above).
    """
    model_config = ConfigDict(arbitrary_types_allowed=True,
                              use_enum_values=True,
                              json_schema_extra={
                                  "$ontology": "https://www.w3.org/TR/vocab-dcat-3/",
                                  "$namespace": str(DCAT),
                                  "$IRI": DCAT.Distribution,
                                  "$prefix": "dcat"
                              }
                              )

    title: List[LiteralField] = Field(
        description="A name given to the distribution.",
        rdf_term=DCTERMS.title,
        rdf_type="rdfs_literal"
    )
    description: List[LiteralField] = Field(
        description="A free-text account of the distribution.",
        rdf_term=DCTERMS.description,
        rdf_type="literal"
    )
    release_date: Union[date, AwareDatetime, NaiveDatetime] = Field(
        default=None,
        description="Date of formal issuance (e.g., publication) of the distribution.",
        rdf_term=DCTERMS.issued,
        rdf_type="datetime_literal"
    )
    update_date: Union[str, date, datetime, AwareDatetime, NaiveDatetime] = Field(
        default=None,
        description="Most recent date on which the distribution was changed, updated or modified.",
        rdf_term=DCTERMS.modified,
        rdf_type="datetime_literal"
    )
    license: AnyHttpUrl = Field(
        default=None,
        description="A legal document under which the distribution is made available.",
        rdf_term=DCTERMS.license,
        rdf_type="uri"
                                )
    access_rights: AnyHttpUrl = Field(
        default=None,
        description='A rights statement that concerns how the distribution is accessed.',
        rdf_term=DCTERMS.accessRights,
        rdf_type="uri")
    rights: [AnyHttpUrl] = Field(
        default=None,
        description="Information about rights held in and over the distribution.",
        rdf_term=DCTERMS.rights,
        rdf_type="uri"
    )
    has_policy: ODRLPolicy = Field(
        default=None,
        description="An ODRL conformant policy expressing the rights associated with the distribution.",
        rdf_term=ODRL2.hasPolicy,
        rdf_type="uri"
    )
    access_url: List[AnyHttpUrl] = Field(
        description="A URL of the resource that gives access to a distribution of the dataset. E.g., landing page, "
                    "feed, SPARQL endpoint.",
        rdf_term=DCAT.accessURL,
        rdf_type="uri"
    )
    access_service: List[Union[AnyHttpUrl, DataService]] = Field(
        default=None,
        description="A data service that gives access to the distribution of the dataset",
        rdf_term=DCAT.accessService,
        rdf_type="uri"
    )
    download_url: List[AnyHttpUrl] = Field(
        default=None,
        description="The URL of the downloadable file in a given format. E.g., CSV file or RDF file. "
                    "The format is indicated by the distribution's dcterms:format and/or dcat:mediaType",
        rdf_term=DCAT.downloadURL,
        rdf_type="uri"
    )
    byte_size: Union[int, LiteralField] = Field(
        default=None,
        description="The size of a distribution in bytes.",
        rdf_term=DCAT.byteSize,
        rdf_type="xsd:nonNegativeInteger."
    )
    spatial_resolution: List[Union[float, LiteralField]] = Field(
        default=None,
        description="Minimum spatial separation resolvable in a dataset distribution, "
                    "measured in meters.",
        rdf_term=DCAT.spatialResolutionInMeters,
        rdf_type="xsd:decimal")
    temporal_resolution: List[Union[str, LiteralField]] = Field(
        default=None,
        description="Minimum time period resolvable in the dataset.",
        rdf_term=DCAT.spatialResolutionInMeters,
        rdf_type="xsd:duration"
    )
    conforms_to: List[AnyHttpUrl] = Field(
        default=None,
        description="An established standard to which the distribution conforms.",
        rdf_term=DCTERMS.conformsTo,
        rdf_type="uri"
    )
    media_type: AnyHttpUrl = Field(
        default=None,
        description="The media type of the distribution as defined by IANA",
        rdf_term=DCAT.mediaType,
        rdf_type="uri"
    )
    format: AnyHttpUrl = Field(
        default=None,
        description="he file format of the distribution.",
        rdf_term=DCTERMS.MediaTypeOrExtent,
        rdf_type="uri"
    )
    compression_format: AnyHttpUrl = Field(
        default=None,
        description="The compression format of the distribution in which the data is contained in a compressed form, "
                    "e.g., to reduce the size of the downloadable file.",
        rdf_term=DCAT.compressFormat,
        rdf_type="uri"
    )
    packaging_format: AnyHttpUrl = Field(
        default=None,
        description="The package format of the distribution in which one or more data files are grouped together, "
                    "e.g., to enable a set of related files to be downloaded together.",
        rdf_term=DCAT.packageFormat,
        rdf_type="uri"
    )
    checksum: Checksum = Field(
        default=None,
        description="The checksum property provides a mechanism that can be used to verify that the contents of "
                    "a file or package have not changed [SPDX].",
        rdf_term=SPDX.checksum,
        rdf_type="uri"
    )

    @field_validator("title", "description", mode="before")
    @classmethod
    def convert_to_literal(cls, value: List[Union[str, LiteralField]]) -> List[LiteralField]:
        return [force_literal_field(item) for item in value]


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "dcat")
    DCATDistribution.save_schema_to_file(Path(json_models_folder, "DCATDistribution.json"), "json")
    DCATDistribution.save_schema_to_file(Path(json_models_folder, "DCATDistribution.yaml"), "yaml")
