from typing import List, Union
from pathlib import Path
from pydantic import Field, AnyHttpUrl, ConfigDict, field_validator
from rdflib.namespace import DCAT, DCTERMS
from dcat.rdf_model import RDFModel, LiteralField
from dcat.vcard import Agent
from utils.validator_functions import force_literal_field


class HRICatalog(RDFModel):
    model_config = ConfigDict(
                              json_schema_extra={
                                  "$ontology": ["https://www.w3.org/TR/vocab-dcat-3/",
                                                "https://health-ri.atlassian.net/wiki/spaces/FSD/pages/121110529/Core+"
                                                "Metadata+Schema+Specification"],
                                  "$namespace": str(DCAT),
                                  "$IRI": DCAT.Catalog,
                                  "$prefix": "dcat"
                              }
                              )
    title: List[LiteralField] = Field(
        description="A name given to the resource.",
        rdf_term=DCTERMS.title,
        rdf_type="rdfs_literal"
    )
    description: List[LiteralField] = Field(
        description="A free-text account of the resource.",
        rdf_term=DCTERMS.description,
        rdf_type="literal"
    )
    publisher: List[Union[AnyHttpUrl, Agent]] = Field(
        description="The entity responsible for making the resource available.",
        rdf_term=DCTERMS.publisher,
        rdf_type="uri"
    )
    dataset: List[AnyHttpUrl] = Field(
        default=None,
        description="relates every catalogue to its containing datasets.",
        rdf_term=DCAT.dataset,
        rdf_type="uri"
    )

    @field_validator("title", "description", mode="before")
    @classmethod
    def convert_to_literal(cls, value: List[Union[str, LiteralField]]) -> List[LiteralField]:
        return [force_literal_field(item) for item in value]


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parent.resolve(), "json_models")
    HRICatalog.save_schema_to_file(Path(json_models_folder, "HRICatalog.json"), "json")
    HRICatalog.save_schema_to_file(Path(json_models_folder, "HRICatalog.yaml"), "yaml")
