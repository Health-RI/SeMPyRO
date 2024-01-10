import json
import ruamel.yaml
from pydantic import BaseModel, Field, TypeAdapter, ConfigDict, EmailStr, Extra
from typing import List, AnyStr, LiteralString, Required, Optional, ClassVar, Union, Dict
from typing_extensions import Annotated

from src.common import BeaconOntologyTerm
from commonDefinitions import (Disease, Ethnicity, Exposure, GeographicLocation, Info, Procedure, Pedigree,
                               Treatment, AgeRange, Sex, KaryotypicSex, PhenotypicFeature, Measurement)


class Individual(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True,
                              json_schema_extra={
                                  "$comment": "version: ga4gh-beacon-individual-v2.0.0",
                                  "$schema": "https://json-schema.org/draft/2020-12/schema"}
                              )
    diseases: List[Disease] = Field(default=None, description="List of disease(s) been diagnosed to the individual, "
                                                              "defined by disease ontology ID(s), age of onset, stage "
                                                              "and the presence of family history.")
    ethnicity: Ethnicity = Field(default=None,
                                 description="Ethnic background of the individual. Value from NCIT Race (NCIT:C17049) "
                                             "ontology term descendants, e.g. NCIT:C126531 (Latin American). A "
                                             "geographic"
                                             "ancestral origin category that is assigned to a population group based "
                                             "mainly on physical characteristics that are thought to be distinct and "
                                             "inherent. [ NCI ] ",
                                 examples=[
                                     {
                                         "id": "NCIT:C42331",
                                         "label": "African"
                                     },
                                     {
                                         "id": "NCIT:C41260",
                                         "label": "Asian"
                                     },
                                     {
                                         "id": "NCIT:C126535",
                                         "label": "Australian"
                                     },
                                     {
                                         "id": "NCIT:C43851",
                                         "label": "European"
                                     },
                                     {
                                         "id": "NCIT:C77812",
                                         "label": "North American"
                                     },
                                     {
                                         "id": "NCIT:C126531",
                                         "label": "Latin American"
                                     },
                                     {
                                         "id": "NCIT:C104495",
                                         "label": "Other race"
                                     }
                                 ]
                                 )
    exposures: List[Exposure] = None
    geographicOrigin: GeographicLocation = Field(default=None,
                                                 description="Individual's country or region of origin (birthplace or "
                                                             "residence place regardless of ethnic origin). Value "
                                                             "from GAZ Geographic Location ontology.",
                                                 examples=[
                                                     {
                                                         "id": "GAZ:00002955",
                                                         "label": "Slovenia"
                                                     },
                                                     {
                                                         "id": "GAZ:00002459",
                                                         "label": "United States of America"
                                                     },
                                                     {
                                                         "id": "GAZ:00316959",
                                                         "label": "Municipality of El Masnou"
                                                     },
                                                     {
                                                         "id": "GAZ:00000460",
                                                         "label": "Eurasia"
                                                     }
                                                 ])
    id: str = Field(description="Individual identifier (internal ID).")
    info: Info = None
    interventionsOrProcedures: List[Procedure] = None
    karyotypicSex: KaryotypicSex = Field(default=None,
                                         description="The chromosomal sex of an individual represented from a "
                                                     "selection of options.")
    measures: List[Measurement] = None
    pedigrees: List[Pedigree] = None
    phenotypicFeatures: List[PhenotypicFeature] = None
    sex: Sex = Field(description="Sex of the individual. Value from NCIT General Qualifier (NCIT:C27993): 'unknown' "
                                 "(not assessed or not available) (NCIT:C17998), 'female' (NCIT:C16576), "
                                 "or 'male', (NCIT:C20197).")
    treatments: List[Treatment] = None


def model_to_file_test():
    individ_model = Individual.model_json_schema()
    # common_element_model = BeaconOntologyTerm.model_json_schema()
    yaml = ruamel.yaml.YAML()

    with open("./beacon/beacon_model.json", "w") as schema_file:
        json.dump(individ_model, schema_file, indent=2)
    with open("./beacon/beacon_model.yaml", "w") as schema_yaml:
        yaml.dump(individ_model, schema_yaml)


if __name__ == "__main__":
    model_to_file_test()
