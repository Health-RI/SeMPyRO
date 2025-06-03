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
from datetime import date
from pathlib import Path
from typing import List, Union, ClassVar, Set

from pydantic import AnyHttpUrl, ConfigDict, Field, field_validator
from rdflib.namespace import DCAT, DCTERMS

from sempyro import LiteralField
from sempyro.dcat import DCATDataService, AccessRights
from sempyro.hri_dcat.hri_dataset import HRIDataset
from sempyro.hri_dcat.hri_agent import HRIAgent
from sempyro.hri_dcat.hri_vcard import HRIVCard
from sempyro.adms import Identifier
from sempyro.hri_dcat.vocabularies import GeonovumLicences, DatasetTheme
from sempyro.namespaces import DCATAPv3, ADMS
from sempyro.utils.validator_functions import convert_to_literal


class HRIDataService(DCATDataService):
    """A collection of operations that provides access to one or more datasets or data processing functions."""
    model_config = ConfigDict(
                              json_schema_extra={
                                  "$ontology": "https://www.w3.org/TR/vocab-dcat-3/",
                                  "$namespace": str(DCAT),
                                  "$IRI": DCAT.DataService,
                                  "$prefix": "dcat"
                              }
                              )
    access_rights: AccessRights = Field(
        description="Information about who access the resource or an indication of its security status.",
        json_schema_extra={
            "rdf_term": DCTERMS.accessRights,
            "rdf_type": "uri"
        }
    )
    applicable_legislation: List[AnyHttpUrl] = Field(
        default=None,
        description="The legislation that is applicable to this resource.",
        json_schema_extra={
            "rdf_term": DCATAPv3.applicableLegislation,
            "rdf_type": "uri"
        }
    )
    application_profile: List[AnyHttpUrl] = Field(
        default=None,
        description="An established standard to which the described resource conforms.",
        json_schema_extra={
            "rdf_term": DCTERMS.conformsTo,
            "rdf_type": "uri"
        }
    )
    contact_point: Union[AnyHttpUrl, HRIVCard] = Field(
        description="Relevant contact information for the cataloged resource.",
        json_schema_extra={
            "rdf_term": DCAT.contactPoint,
            "rdf_type": "uri"
        }
    )
    creator: List[Union[AnyHttpUrl, HRIAgent]] = Field(
        default=None,
        description="An entity responsible for making the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.creator,
            "rdf_type": "uri"
        }
    )
    rights: List[AnyHttpUrl] = Field(
        default=None,
        description="Information about rights held in and over the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.rights,
            "rdf_type": "uri"
        }
    )
    endpoint_url: AnyHttpUrl = Field(
        description="The root location or primary endpoint of the service (a Web-resolvable IRI).",
        json_schema_extra={
            "rdf_term": DCAT.endpointURL,
            "rdf_type": "uri"
        }
    )
    format: List[AnyHttpUrl] = Field(
        default=None,
        description="The file format, physical medium, or dimensions of the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.format,
            "rdf_type": "uri"
        }
    )
    hvd_category: List[AnyHttpUrl] = Field( # IRI or skos:Concept
        default=None,
        description="A data category defined in the High Value Dataset Implementing Regulation.",
        json_schema_extra={
            "rdf_term": DCATAPv3.hvdCategory,
            "rdf_type": "uri"
        }
    )
    other_identifier: List[Union[AnyHttpUrl, Identifier]] = Field(
        default=None,
        description="Links a resource to an adms:Identifier class.",
        json_schema_extra={
            "rdf_term": ADMS.identifier,
            "rdf_type": "uri"
        }
    )
    serves_dataset: List[Union[AnyHttpUrl, HRIDataset]] = Field(
        default=None,
        description="A collection of data that this data service can distribute.",
        json_schema_extra={
            "rdf_term": DCAT.servesDataset,
            "rdf_type": "uri"
        }
    )
    endpoint_description: AnyHttpUrl = Field(
        description="A description of the services available via the end-points, including their operations, "
                    "parameters etc.",
        json_schema_extra={
            "rdf_term": DCAT.endpointDescription,
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
    license: Union[AnyHttpUrl, GeonovumLicences] = Field(
        description="A legal document giving official permission to do something with the resource.",
        json_schema_extra={
            "rdf_term": DCTERMS.license,
            "rdf_type": "uri"
        }
    )
    publisher: Union[AnyHttpUrl, HRIAgent] = Field(
        description="The entity responsible for making the resource available.",
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


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "hri_dcat")
    HRIDataService.save_schema_to_file(Path(json_models_folder, "HRIDataService.json"), "json")
    HRIDataService.save_schema_to_file(Path(json_models_folder, "HRIDataService.yaml"), "yaml")
