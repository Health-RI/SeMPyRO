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
from typing import List, Union, ClassVar, Set

from pydantic import AnyHttpUrl, ConfigDict, Field, field_validator
from rdflib.namespace import DCAT, DCTERMS, FOAF, PROV

from sempyro import LiteralField
from sempyro.dcat import DCATDataset, AccessRights, DCATDistribution, DCATDatasetSeries, Attribution, Relationship
from sempyro.dqv import QualityCertificate
from sempyro.adms import Identifier
from sempyro.hri_dcat.hri_agent import HRIAgent
from sempyro.hri_dcat.hri_vcard import HRIVCard
from sempyro.hri_dcat.vocabularies import DatasetTheme, DatasetStatus
from sempyro.namespaces import DCATv3, DCATAPv3, HEALTHDCATAP, DPV, ADMS, DQV
from sempyro.time import PeriodOfTime
from sempyro.utils.validator_functions import convert_to_literal


class HRIDataset(DCATDataset):
    model_config = ConfigDict(
                              json_schema_extra={
                                  "$ontology": ["https://www.w3.org/TR/vocab-dcat-3/",
                                                "https://health-ri.atlassian.net/wiki/spaces/FSD/pages/121110529/Core+"
                                                "Metadata+Schema+Specification"],
                                  "$namespace": str(DCAT),
                                  "$IRI": DCAT.Dataset,
                                  "$prefix": "dcat"
                              }
                              )

    access_rights: AccessRights = Field(
        description="Information about who can access the resource or an indication of its security status.",
        json_schema_extra={
            "rdf_term": DCTERMS.accessRights,
            "rdf_type": "uri"
        }
    )

    analytics: List[Union[AnyHttpUrl, DCATDistribution]] = Field(
        default=None,
        description="An analytics distribution of the dataset.",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.analytics,
            "rdf_type": "uri"
        }
    )

    applicable_legislation: List[AnyHttpUrl] = Field(
        description="The legislation that is applicable to this resource.",
        json_schema_extra={
            "rdf_term": DCATAPv3.applicableLegislation,
            "rdf_type": "uri",
            # "bind_namespace": ['dcatap', DCATAPv3]
        }
    )

    contact_point: Union[AnyHttpUrl, HRIVCard] = Field(
        description="Relevant contact information for the cataloged resource.",
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
            "rdf_type": "uri"
        }
    )

    coding_system: List[AnyHttpUrl] = Field(
        default=None,
        description="Health classifications and their codes associated with the dataset",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.hasCodingSystem,
            "rdf_type": "uri"
        }
    )

    conforms_to: List[AnyHttpUrl] = Field(
        default=None,
        description="An established standard to which the described resource conforms.",
        json_schema_extra={
            "rdf_term": DCTERMS.conformsTo,
            "rdf_type": "uri"
        }
    )

    creator: List[Union[AnyHttpUrl, HRIAgent]] = Field(
        description="The entity responsible for producing the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.creator,
            "rdf_type": "uri"
        }
    )
    distribution: List[Union[AnyHttpUrl, DCATDistribution]] = Field(
        default=None,
        description="An available Distribution for the Dataset.",
        json_schema_extra={
            "rdf_term": DCAT.distribution,
            "rdf_type": "uri"
        }
    )

    documentation: List[AnyHttpUrl] = Field(
        default=None,
        description="A page or document about this thing.",
        json_schema_extra={
            "rdf_term": FOAF.page,
            "rdf_type": "uri"
        }
    )

    # Frequency uses another vocabulary then the DCAT Dataset.
    frequency: AnyHttpUrl = Field(
        default=None,
        description="The frequency at which a dataset is published.",
        json_schema_extra={
            "rdf_term": DCTERMS.accrualPeriodicity,
            "rdf_type": "uri"
        }
    )

    health_theme: List[AnyHttpUrl] = Field(
        default=None,
        description="A category of the Dataset or tag describing the Dataset.",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.healthTheme,
            "rdf_type": "uri"
        }
    )

    in_series: List[Union[DCATDatasetSeries, AnyHttpUrl]] = Field(
        default=None,
        description="A dataset series of which the dataset is part.",
        json_schema_extra={
            "rdf_term": DCATv3.inSeries,
            "rdf_type": "uri"
        }
    )

    is_referenced_by: List[AnyHttpUrl] = Field(
        default=None,
        description="A related resource that references, cites, or otherwise points to the described resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.isReferencedBy,
            "rdf_type": "uri"
        }
    )

    legal_basis: List[AnyHttpUrl] = Field(
        default=None,
        description="Indicates use or applicability of a Legal Basis.",
        json_schema_extra={
            "rdf_term": DPV.hasLegalBasis,
            "rdf_type": "uri"
        }
    )

    maximum_typical_age: Union[int, LiteralField] = Field(
        default=None,
        description="Maximum typical age of the population within the dataset.",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.maxTypicalAge,
            "rdf_type": "xsd:nonNegativeInteger"
        }
    )

    minimum_typical_age: Union[int, LiteralField] = Field(
        default=None,
        description="Minimum typical age of the population within the dataset",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.minTypicalAge,
            "rdf_type": "xsd:nonNegativeInteger"
        }
    )

    number_of_records: Union[int, LiteralField] = Field(
        default=None,
        description="Size of the dataset in terms of the number of records",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.numberOfRecords,
            "rdf_type": "xsd:nonNegativeInteger"
        }
    )

    number_of_unique_individuals: Union[int, LiteralField] = Field(
        default=None,
        description="Number of records for unique individuals.",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.numberOfUniqueIndividuals,
            "rdf_type": "xsd:nonNegativeInteger"
        }
    )

    other_identifier: Identifier = Field(
        default=None,
        description="Number of records forLinks a resource to an adms:Identifier class. unique individuals.",
        json_schema_extra={
            "rdf_term": ADMS.identifier,
            "rdf_type": "uri"
        }
    )

    personal_data: List[AnyHttpUrl] = Field(
        default=None,
        description="Indicates association with Personal Data.",
        json_schema_extra={
            "rdf_term": DPV.hasPersonalData,
            "rdf_type": "uri"
        }
    )

    population_coverage: Union[str, LiteralField] = Field(
        default=None,
        description="A definition of the population within the dataset",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.populationCoverage,
            "rdf_type": "rdfs_literal"
        }
    )

    purpose: List[AnyHttpUrl] = Field(
        default=None,
        description="Indicates association with Purpose.",
        json_schema_extra={
            "rdf_term": DPV.hasPurpose,
            "rdf_type": "uri"
        }
    )

    qualified_attribution: List[Union[AnyHttpUrl, Attribution]] = Field(
        default=None,
        description="Attribution is the ascribing of an entity to an agent.",
        json_schema_extra={
            "rdf_term": PROV.qualifiedAttribution,
            "rdf_type": "uri"
        }
    )

    qualified_relation: List[Union[AnyHttpUrl, Relationship]] = Field(
        default=None,
        description="Link to a description of a relationship with another resource.",
        json_schema_extra={
            "rdf_term": DCAT.qualifiedRelation,
            "rdf_type": "uri"
        }
    )

    quality_annotation: List[Union[AnyHttpUrl, QualityCertificate]] = Field(
        default=None,
        description="Refers to a quality annotation.",
        json_schema_extra={
            "rdf_term": DQV.hasQualityAnnotation,
            "rdf_type": "uri"
        }
    )

    retention_period: PeriodOfTime = Field(
        default=None,
        description="A temporal period which the dataset is available for secondary use.",
        json_schema_extra={
            "rdf_term": HEALTHDCATAP.retentionPeriod,
            "rdf_type": DCTERMS.PeriodOfTime,
        }
    )

    sample: List[Union[AnyHttpUrl, DCATDistribution]] = Field(
        default=None,
        description="Links to a sample of an Asset (which is itself an Asset).",
        json_schema_extra={
            "rdf_term": ADMS.sample,
            "rdf_type": "uri"
        }
    )

    source: List[Union[AnyHttpUrl, DCATDataset]] = Field(
        default=None,
        description="A related resource from which the described resource is derived.",
        json_schema_extra={
            "rdf_term": DCTERMS.source,
            "rdf_type": "uri"
        }
    )

    status: DatasetStatus = Field(
        default=None,
        description="The status of the Asset in the context of a particular workflow process.",
        json_schema_extra={
            "rdf_term": ADMS.status,
            "rdf_type": "uri"
        }
    )
    identifier: Union[str, LiteralField] = Field(
        description="An unambiguous reference to the resource within a given context.",
        json_schema_extra={
            "rdf_term": DCTERMS.identifier,
            "rdf_type": "rdfs_literal"
        }
    )
    publisher: Union[AnyHttpUrl, HRIAgent] = Field(
        description="An entity responsible for making the resource available.",
        json_schema_extra={
            "rdf_term": DCTERMS.publisher,
            "rdf_type": "uri"
        }
    )
    theme: List[DatasetTheme] = Field(
        description="A main category of the resource. A resource can have multiple themes.",
        json_schema_extra={
            "rdf_term": DCAT.theme,
            "rdf_type": "uri"
        }
    )
    type: List[AnyHttpUrl] = Field(
        default=None,
        description="The nature or genre of the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.type,
            "rdf_type": "uri"
        }
    )

    keyword: List[LiteralField] = Field(
        description="A keyword or tag describing the resource.",
        json_schema_extra={
            "rdf_term": DCAT.keyword,
            "rdf_type": "rdfs_literal"
        }
    )


    _validate_literal_fields: ClassVar[Set[str]] = DCATDataset._validate_literal_fields | {"keyword", "population_coverage"}

    @field_validator(*_validate_literal_fields, mode="before")
    @classmethod
    def validate_literal(cls, value: List[Union[str, LiteralField]]) -> List[LiteralField]:
        return convert_to_literal(value)


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "hri_dcat")
    HRIDataset.save_schema_to_file(Path(json_models_folder, "HRIDataset.json"), "json")
    HRIDataset.save_schema_to_file(Path(json_models_folder, "HRIDataset.yaml"), "yaml")
