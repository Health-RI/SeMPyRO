import dateutil.parser as parser
from datetime import date, datetime
from typing import List, Union
from pathlib import Path
from pydantic import Field, AnyHttpUrl, ConfigDict, AwareDatetime, NaiveDatetime, ValidationError, field_validator
import re
from rdflib.namespace import DCAT, DCTERMS, FOAF
from dcat.rdf_model import RDFModel, LiteralField
from dcat.vcard import Agent

from namespaces.DCATv3 import DCATv3


class HRIDataset(RDFModel):
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
    contact_point: List[Union[AnyHttpUrl, Agent]] = Field(
        description="Relevant contact information for the cataloged resource.",
        rdf_term=DCAT.contactPoint,
        rdf_type="uri")

    creator: List[Union[AnyHttpUrl, Agent]] = Field(
        description="The entity responsible for producing the resource. Resources of type foaf:Agent are "
                    "recommended as values for this property.",
        rdf_term=DCTERMS.creator,
        rdf_type="uri")

    description: List[LiteralField] = Field(
        description="A free-text account of the resource.",
        rdf_term=DCTERMS.description,
        rdf_type="literal"
    )
    issued: Union[str, datetime, date, AwareDatetime, NaiveDatetime] = Field(
        description="Date of formal issuance (e.g., publication) of the resource.",
        alias="release_date",
        rdf_term=DCTERMS.issued,
        rdf_type="datetime_literal"
    )
    identifier: Union[str, LiteralField] = Field(
        description="A unique identifier of the resource being described or cataloged.",
        rdf_term=DCTERMS.identifier,
        rdf_type="xsd:string")
    modified: Union[str, date, AwareDatetime, NaiveDatetime] = Field(
        description="Most recent date on which the resource was changed, updated or modified.",
        alias="modification_date",
        rdf_term=DCTERMS.modified,
        rdf_type="datetime_literal"
    ) # todo if empty populate from issued
    publisher: List[Union[AnyHttpUrl, Agent]] = Field(
        description="The entity responsible for making the resource available.",
        rdf_term=DCTERMS.publisher,
        rdf_type="uri"
    )
    theme: List[AnyHttpUrl] = Field(
        description="A main category of the resource. A resource can have multiple themes.",
        alias="category",
        rdf_term=DCAT.themeTaxonomy,
        rdf_type="uri"
    )
    title: List[LiteralField] = Field(
        description="A name given to the resource.",
        rdf_term=DCTERMS.title,
        rdf_type="rdfs_literal"
    )
    type: List[AnyHttpUrl] = Field(
        description="The nature or genre of the resource.",
        alias="genre",
        rdf_term=DCTERMS.type,
        rdf_type="uri")
    license: AnyHttpUrl = Field(
        description="A legal document under which the resource is made available.",
        rdf_term=DCTERMS.license,
        rdf_type="uri"
    )
    relation: List[AnyHttpUrl] = Field(
        description="A resource with an unspecified relationship to the cataloged resource.",
        rdf_term=DCTERMS.relation,
        rdf_type="uri"
    )
    distribution: List[AnyHttpUrl] = Field(
        default=None,
        description="An available distribution of the dataset.",
        rdf_term=DCAT.distribution,
        rdf_type="uri"
    )
    project: List[AnyHttpUrl] = Field(
        default=None,
        description="connect dataset to the corresponding projects",
        rdf_term=FOAF.Project,
        rdf_type="uri"
    )
    has_version: List[AnyHttpUrl] = Field(
        default=None,
        description="This resource has a more specific, versioned resource",
        rdf_term=DCTERMS.hasVersion,
        rdf_type="uri"
    )
    in_series: List[AnyHttpUrl] = Field(
        default=None,
        description="A dataset series of which the dataset is part.",
        rdf_term=DCATv3.inSeries,
        rdf_type="uri"
    )

    @field_validator("issued", mode="before")
    @classmethod
    def date_handler(cls, value):
        if isinstance(value, str):
            year_pattern = re.compile("-?([1-9][0-9]{3,}|0[0-9]{3})(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?")
            year_month_pattern = re.compile("-?([1-9][0-9]{3,}|0[0-9]{3})-(0[1-9]|1[0-2])(Z|(\+|-)((0[0-9]|1[0-3]):"
                                            "[0-5][0-9]|14:00))?")
            if not (re.match(year_pattern, value) or re.match(year_month_pattern, value)):
                try:
                    value = parser.parse(value)
                except TypeError:
                    raise ValidationError
        return value


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parent.resolve(), "json_models")
    HRIDataset.save_schema_to_file(Path(json_models_folder, "HRIDataset.json"), "json")
    HRIDataset.save_schema_to_file(Path(json_models_folder, "HRIDataset.yaml"), "yaml")
