from pydantic import BaseModel, Field, TypeAdapter, ConfigDict, EmailStr, Extra
from typing import List, AnyStr, LiteralString, Required, Optional
from typing_extensions import Annotated
from enum import Enum

from src.common import BeaconOntologyTerm


class Sex(str, Enum):
    female = "NCIT:C16576"
    male = "NCIT:C20197"
    unknown = "NCIT:C1799"


class TimeElement(BaseModel):
    pass


Age = Annotated[str, Field(description="Represents age as a ISO8601 duration (e.g., 'P40Y10M05D').", exclude=True)]
# regexpr?
age = TypeAdapter(Age)


class AgeRange(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed = True)
    end: Age = Field(description="Represents age as a ISO8601 duration (e.g., 'P40Y10M05D').",
                     examples=['P40Y10M05D'])
    start: Age = Field(
        description="Represents age as a ISO8601 duration (e.g., 'P40Y10M05D').")


class Disease(BaseModel):
    diseaseCode: str
    ageOfOnset: TimeElement


class Ethnicity(BeaconOntologyTerm):
    pass


class Exposure(BaseModel):
    pass


class GeographicLocation(BeaconOntologyTerm):
    pass


class Info(BaseModel):
    pass


class Procedure(BaseModel):
    pass


class KaryotypicSex(BaseModel):
    pass


class Measurement(BaseModel):
    pass


class Pedigree(BaseModel):
    pass


class PhenotypicFeature(BaseModel):
    pass


class Treatment(BaseModel):
    pass
