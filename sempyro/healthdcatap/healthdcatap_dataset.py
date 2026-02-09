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
from typing import ClassVar, List, Set, Union

from pydantic import AnyHttpUrl, ConfigDict, Field, field_validator
from rdflib.namespace import DCAT, DCTERMS

from sempyro import LiteralField
from sempyro.dcat import DCATDataset
from sempyro.healthdcatap.healthdcatap_kind import HEALTHDCATAPKind
from sempyro.healthdcatap.healthdcatap_agent import HEALTHDCATAPAgent
from sempyro.healthdcatap.healthdcatap_hdab import HEALTHDCATAPHdab
from sempyro.healthdcatap.healthdcatap_publisher import HEALTHDCATAPPublisher
from sempyro.healthdcatap.healthdcatap_distribution import HEALTHDCATAPDistribution
from sempyro.namespaces import HEALTHDCATAP, DPV, DCATAPv3
from sempyro.time import PeriodOfTime
from sempyro.utils.validator_functions import convert_to_literal


class HEALTHDCATAPDataset(DCATDataset):
    model_config = ConfigDict(
        json_schema_extra={
            "$ontology": [
                "https://www.w3.org/TR/vocab-dcat-3/",
                "https://healthdataeu.pages.code.europa.eu/healthdcat-ap/releases/release-5/",
            ],
            "$namespace": str(DCAT),
            "$IRI": DCAT.Dataset,
            "$prefix": "dcat",
        }
    )

    access_rights: AnyHttpUrl = Field(
        description="Information about who can access the dataset and under what conditions.",
        json_schema_extra={
            "rdf_term": DCTERMS.accessRights,
            "rdf_type": "uri"
        }
    )
    applicable_legislation: List[AnyHttpUrl] = Field(
        description="The legislation that mandates the creation or management of the dataset.",
        json_schema_extra={
            "rdf_term": DCATAPv3.applicableLegislation,
            "rdf_type": "uri"
        },
    )
    analytics: List[Union[AnyHttpUrl, HEALTHDCATAPDistribution]] = Field(
        default=None,
        description="An analytics distribution of the dataset.",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.analytics,
            "rdf_type": "uri",
        },
    )
    contact_point: List[Union[HEALTHDCATAPKind, AnyHttpUrl]] = Field(
        description="Relevant contact information for the cataloged resource. Use of vCard is recommended",
        json_schema_extra={
            "rdf_term": DCAT.contactPoint,
            "rdf_type": "uri"
        }
    )
    code_values: List[AnyHttpUrl] = Field(
        default=None,
        description="Coding systems in use (ex: ICD-10-CM, DGRs, SNOMED=CT, ...)",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.hasCodeValues,
            "rdf_type": "uri",
        },
    )
    coding_system: List[AnyHttpUrl] = Field(
        default=None,
        description="Health classifications and their codes associated with the dataset",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.hasCodingSystem,
            "rdf_type": "uri",
        },
    )
    creator: List[Union[HEALTHDCATAPAgent, AnyHttpUrl]] = Field(
        default=None,
        description="The entity responsible for producing the resource. Resources of type foaf:Agent are "
                    "recommended as values for this property.",
        json_schema_extra={
            "rdf_term": DCTERMS.creator,
            "rdf_type": "uri"
        }
    )
    distribution: List[AnyHttpUrl] = Field(
        description="An available distribution of the dataset.",
        json_schema_extra={
            "rdf_term": DCAT.distribution,
            "rdf_type": "uri"
        }
    )
    health_theme: List[AnyHttpUrl] = Field(
        default=None,
        description="A category of the Dataset or tag describing the Dataset.",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.healthTheme,
            "rdf_type": "uri",
        },
    )
    health_category: List[AnyHttpUrl] = Field(
        description="The health category to which this dataset belongs.",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.healthCategory,
            "rdf_type": "uri",
        },
    )
    identifier: List[Union[str, LiteralField]] = Field(
        description="A unique identifier of the resource being described or cataloged.",
        json_schema_extra={
            "rdf_term": DCTERMS.identifier,
            "rdf_type": "rdfs_literal"
        }
    )
    hdab: Union[AnyHttpUrl, HEALTHDCATAPHdab] = Field(
        default=None,
        description="Health Data Access Body supporting access to data in the Member State.",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.hdab,
            "rdf_type": "uri",
        },
    )
    legal_basis: List[AnyHttpUrl] = Field(
        default=None,
        description="The legal basis used to justify processing of personal data.",
        json_schema_extra={
            "rdf_term": DPV.hasLegalBasis,
            "rdf_type": "uri",
        },
    )
    publisher: List[Union[AnyHttpUrl, HEALTHDCATAPPublisher]] = Field(
        default=None,
        description="Agent responsible for making the health data resource available.",
        json_schema_extra={
            "rdf_term": DCTERMS.publisher,
            "rdf_type": "uri",
        },
    )
    maximum_typical_age: Union[int, LiteralField] = Field(
        default=None,
        description="Maximum typical age of the population within the dataset.",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.maxTypicalAge,
            "rdf_type": "xsd:nonNegativeInteger",
        },
    )
    minimum_typical_age: Union[int, LiteralField] = Field(
        default=None,
        description="Minimum typical age of the population within the dataset",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.minTypicalAge,
            "rdf_type": "xsd:nonNegativeInteger",
        },
    )
    number_of_records: Union[int, LiteralField] = Field(
        default=None,
        description="Size of the dataset in terms of the number of records",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.numberOfRecords,
            "rdf_type": "xsd:nonNegativeInteger",
        },
    )
    number_of_unique_individuals: Union[int, LiteralField] = Field(
        default=None,
        description="Number of records for unique individuals.",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.numberOfUniqueIndividuals,
            "rdf_type": "xsd:nonNegativeInteger",
        },
    )
    population_coverage: List[Union[str, LiteralField]] = Field(
        default=None,
        description="A definition of the population within the dataset",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.populationCoverage,
            "rdf_type": "rdfs_literal",
        },
    )
    retention_period: PeriodOfTime = Field(
        default=None,
        description="A temporal period which the dataset is available for secondary use.",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.retentionPeriod,
            "rdf_type": DCTERMS.PeriodOfTime,
        },
    )
    _validate_literal_fields: ClassVar[Set[str]] = DCATDataset._validate_literal_fields | {"population_coverage"}

    @field_validator(*_validate_literal_fields, mode="before")
    @classmethod
    def validate_literal(cls, value: List[Union[str, LiteralField]]) -> List[LiteralField]:
        return convert_to_literal(value)


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "health_dcat")
    HEALTHDCATAPDataset.save_schema_to_file(Path(json_models_folder, "HEALTHDCATAPDataset.json"), "json")
    HEALTHDCATAPDataset.save_schema_to_file(Path(json_models_folder, "HEALTHDCATAPDataset.yaml"), "yaml")
