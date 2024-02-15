from pydantic import ConfigDict, AnyHttpUrl, Field
from dcat.rdf_model import RDFModel, LiteralField
from rdflib import Namespace
from pathlib import Path
from typing import Union


SPDX = Namespace("http://spdx.org/rdf/terms#")


class Checksum(RDFModel):
    """
    A Checksum is value that allows the contents of a file to be authenticated. 
    Even small changes to the content of the file will change its checksum. 
    This class allows the results of a variety of checksum and cryptographic message digest algorithms to be 
    represented.
    """
    model_config = ConfigDict(json_schema_extra={
                                  "$ontology": "http://spdx.org/rdf/terms/2.3",
                                  "$namespace": str(SPDX),
                                  "$IRI": SPDX.Checksum,
                                  "$prefix": "spdx"
                              }
                              )

    algorithm: AnyHttpUrl = Field(
        description="The algorithm used to produce the subject Checksum.",
        rdf_term=SPDX.algorithm,
        rdf_type="uri"
                           )
    checksum_value: Union[str, LiteralField] = Field(
        description="A lower case hexadecimal encoded digest value produced using a specific algorithm.",
        rdf_term=SPDX.checksumValue,
        rdf_type="xsd:hexBinary"
    )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parent.resolve(), "json_models")
    Checksum.save_schema_to_file(Path(json_models_folder, "Checksum.json"), "json")
    Checksum.save_schema_to_file(Path(json_models_folder, "Checksum.yaml"), "yaml")

