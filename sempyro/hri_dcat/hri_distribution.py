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
from typing import List, Union

from pydantic import AnyHttpUrl, ConfigDict, Field, AwareDatetime, NaiveDatetime
from rdflib.namespace import DCAT, DCTERMS, FOAF

from sempyro import LiteralField
from sempyro.dcat import DCATDistribution
from sempyro.hri_dcat import HRIDataService
from sempyro.hri_dcat.vocabularies import GeonovumLicences, DistributionStatus
from sempyro.namespaces import DCATAPv3, ADMS
from sempyro.time import PeriodOfTime


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
    applicable_legislation: List[AnyHttpUrl] = Field(
        default=None,
        description="The legislation that is applicable to this resource.",
        json_schema_extra={
            "rdf_term": DCATAPv3.applicableLegislation,
            "rdf_type": "uri",
            # "bind_namespace": ['dcatap', DCATAPv3]
        }
    )
    documentation: List[AnyHttpUrl] = Field(
        default=None,
        description="Additional documentation about the distribution.",
        json_schema_extra={
            "rdf_term": FOAF.page,
            "rdf_type": "uri"
        }
    )
    access_rights: AnyHttpUrl = Field(
        default=None,
        description="A data service that gives access to the distribution of the dataset.",
        json_schema_extra={
            "rdf_term": DCTERMS.accessRights,
            "rdf_type": "uri"
        }
    )
    language: List[AnyHttpUrl] = Field(
        default=None,
        description="A language of the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.language,
            "rdf_type": "uri"
        }
    )
    linked_schemas: List[AnyHttpUrl] = Field(
        default=None,
        description="An established standard to which the described resource conforms.",
        json_schema_extra={
            "rdf_term": DCTERMS.conformsTo,
            "rdf_type": "uri"
        }
    )

    modification_date: Union[str, date, AwareDatetime, NaiveDatetime] = Field(
        default=None,
        description="Most recent date on which the resource was changed, updated or modified.",
        json_schema_extra={
            "rdf_term": DCTERMS.modified,
            "rdf_type": "datetime_literal"
        }
    )

    release_date: Union[str, datetime, date, AwareDatetime, NaiveDatetime] = Field(
        default=None,
        description="Date of formal issuance (e.g., publication) of the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.issued,
            "rdf_type": "datetime_literal"
        }
    )
    retention_period: List[Union[AnyHttpUrl, PeriodOfTime]] = Field(
        default=None,
        description="A temporal period which the dataset is available for secondary use.",
        json_schema_extra={
            "rdf_term": DCTERMS.accrualPeriodicity,  # consider `dct:PeriodOfTime` if defined elsewhere
            "rdf_type": "uri"
        }
    )
    status: Union[AnyHttpUrl, DistributionStatus] = Field(
        default=None,
        description="The status of the distribution (e.g., under development, completed, deprecated, withdrawn).",
        json_schema_extra={
            "rdf_term": ADMS.status,
            "rdf_type": "uri"
        }
    )



if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "hri_dcat")
    HRIDistribution.save_schema_to_file(Path(json_models_folder, "HRIDistribution.json"), "json")
    HRIDistribution.save_schema_to_file(Path(json_models_folder, "HRIDistribution.yaml"), "yaml")
