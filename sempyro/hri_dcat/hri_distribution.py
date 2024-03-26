from pathlib import Path
from typing import List, Union

from sempyro.dcat.data_service import DataService
from sempyro.rdf_model import RDFModel, LiteralField
from pydantic import Field, AnyHttpUrl, ConfigDict, field_validator
from rdflib.namespace import DCAT, DCTERMS

from sempyro.utils.validator_functions import force_literal_field


class HRIDistribution(RDFModel):
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
        description="A name given to the distribution.",
        rdf_term=DCTERMS.title,
        rdf_type="rdfs_literal"
    )
    description: List[LiteralField] = Field(
        description="A free-text account of the distribution.",
        rdf_term=DCTERMS.description,
        rdf_type="rdfs_literal"
    )
    access_url: List[AnyHttpUrl] = Field(
        description="A URL of the resource that gives access to a distribution of the dataset. E.g., landing page, "
                    "feed, SPARQL endpoint.",
        rdf_term=DCAT.accessURL,
        rdf_type="uri"
    )
    media_type: AnyHttpUrl = Field(
        description="The media type of the distribution as defined by IANA",
        rdf_term=DCAT.mediaType,
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

    @field_validator("title", "description", mode="before")
    @classmethod
    def convert_to_literal(cls, value: List[Union[str, LiteralField]]) -> List[LiteralField]:
        return [force_literal_field(item) for item in value]


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parent.resolve(), "json_models")
    HRIDistribution.save_schema_to_file(Path(json_models_folder, "HRIDistribution.json"), "json")
    HRIDistribution.save_schema_to_file(Path(json_models_folder, "HRIDistribution.yaml"), "yaml")
