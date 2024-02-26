from pathlib import Path
from pydantic import ConfigDict, AnyHttpUrl, Field, field_validator
from rdflib.namespace import DCAT, DCTERMS
from typing import List, Union

from dcat.dcat_resource import DCATResource
from dcat.rdf_model import RDFModel, LiteralField
from hri_dataset import HRIDataset
from utils.validator_functions import force_literal_field


class HRIDataService(RDFModel):
    """A collection of operations that provides access to one or more datasets or data processing functions."""
    model_config = ConfigDict(
                              json_schema_extra={
                                  "$ontology": "https://www.w3.org/TR/vocab-dcat-3/",
                                  "$namespace": str(DCAT),
                                  "$IRI": DCAT.DataService,
                                  "$prefix": "dcat"
                              }
                              )
    endpoint_url: List[Union[AnyHttpUrl, DCATResource]] = Field(
        description="The root location or primary endpoint of the service (a Web-resolvable IRI).",
        rdf_term=DCAT.endpointURL,
        rdf_type="uri"
    )
    title: List[LiteralField] = Field(
        description="A name given to the resource.",
        rdf_term=DCTERMS.title,
        rdf_type="rdfs_literal"
    )
    serves_dataset: List[Union[AnyHttpUrl, HRIDataset]] = Field(
        description="A collection of data that this data service can distribute.",
        rdf_term=DCAT.servesDataset,
        rdf_type="uri"
    )
    endpoint_description: List[Union[AnyHttpUrl, DCATResource, LiteralField]] = Field(
        default=None,
        description="A description of the services available via the end-points, including their operations, "
                    "parameters etc.",
        rdf_term=DCAT.endpointDescription,
        rdf_type="uri"
    )

    @field_validator("title", "endpoint_description", mode="before")
    @classmethod
    def convert_to_literal(cls, value: List[Union[str, LiteralField]]) -> List[LiteralField]:
        return [force_literal_field(item) for item in value]


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parent.resolve(), "json_models")
    HRIDataService.save_schema_to_file(Path(json_models_folder, "HRIDataService.json"), "json")
    HRIDataService.save_schema_to_file(Path(json_models_folder, "HRIDataService.yaml"), "yaml")