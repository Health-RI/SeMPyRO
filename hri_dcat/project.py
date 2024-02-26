from typing import List, Union
from pathlib import Path
from pydantic import Field, AnyHttpUrl, ConfigDict
from rdflib.namespace import DCTERMS, FOAF
from dcat.rdf_model import RDFModel, LiteralField
from dcat.vcard import Agent


class Project(RDFModel):
    model_config = ConfigDict(
                              json_schema_extra={
                                  "$ontology": ["http://xmlns.com/foaf/spec/",
                                                "https://health-ri.atlassian.net/wiki/spaces/FSD/pages/121110529/Core+"
                                                "Metadata+Schema+Specification"],
                                  "$namespace": str(FOAF),
                                  "$IRI": FOAF.Project,
                                  "$prefix": "foaf"
                              }
                              )
    description: List[LiteralField] = Field(
        description="A free-text description of the project.",
        rdf_term=DCTERMS.description,
        rdf_type="literal"
    )
    identifier: Union[str, LiteralField] = Field(
        description="A unique identifier of the resource being described or cataloged.",
        rdf_term=DCTERMS.identifier,
        rdf_type="xsd:string"
    )
    title: List[LiteralField] = Field(
        description="A name given to the resource.",
        rdf_term=DCTERMS.title,
        rdf_type="rdfs_literal"
    )
    founded_by: List[Union[AnyHttpUrl, Agent]] = Field(
        description="An organization funding a project or person.",
        rdf_term=FOAF.fundedBy,
        rdf_type="uri"
    )
    relation: List[AnyHttpUrl] = Field(
        description="Link to the project datasets",
        rdf_term=DCTERMS.relation,
        rdf_type="uri"
    )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parent.resolve(), "json_models")
    Project.save_schema_to_file(Path(json_models_folder, "Project.json"), "json")
    Project.save_schema_to_file(Path(json_models_folder, "Project.yaml"), "yaml")
