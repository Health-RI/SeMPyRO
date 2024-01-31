import logging
import typing

from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Union, ClassVar, Type, Dict, Any
from pydantic import (BaseModel, Field, validator, AwareDatetime, NaiveDatetime, AnyHttpUrl, field_validator,
                      model_validator)
from rdflib import BNode, Graph, Namespace, URIRef, Literal
from rdflib.namespace import DCAT, DCTERMS, RDF, XSD, RDFS, TIME, DefinedNamespace
from typing_extensions import Annotated
from pydantic.fields import PydanticUndefined

from dcat.rdf_model import RDFModel, RDFModelError, LiteralField

import ruamel.yaml
import json

from enum import Enum

from datetime import date, datetime, time

logger = logging.getLogger("__name__")

RDF_KEY = "rdf_term"
RDF_TYPE_KEY = "rdf_type"

GREG_URL = "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"


class TimePosition(RDFModel):
    """
    A temporal position described using either a (nominal) value from an ordinal reference system,
    or a (numeric) value in a temporal coordinate system.
    """
    model_config = ConfigDict(title=TIME.TimePosition)
    nominalPosition: str = Field(default=None,
                                 description="The (nominal) value indicating temporal position in an ordinal reference "
                                             "system",
                                 rdf_term=TIME.nominalPosition,
                                 rdf_type="xsd:string")
    numericPosition: float = Field(default=None,
                                   description="The (numeric) value indicating position within a temporal coordinate "
                                               "system",
                                   rdf_term=TIME.numericPosition,
                                   rdf_type="xsd:decimal"
                                   )
    hasTRS: AnyHttpUrl = Field(description="The temporal reference system used by a temporal position or extent "
                                           "description",
                               rdf_term=TIME.hasTRS,
                               rdf_type="uri"
                               )

    @model_validator(mode="before")
    @classmethod
    def validate(cls, data: Dict) -> Dict[str, Any]:
        if data.get("nominalPosition") and data.get("numericPosition"):
            raise ValueError("Expected only one, either `nominalPosition` or `numericPosition`, both were provided")
        elif data.get("nominalPosition") is None and data.get("numericPosition") is None:
            raise ValueError("Either `nominalPosition` or `numericPosition` should be provided")
        return data


class DayOfWeek(Enum):
    Monday = TIME.Monday
    Tuesday = TIME.Tuesday
    Wednesday = TIME.Wednesday
    Thursday = TIME.Thursday
    Friday = TIME.Friday
    Saturday = TIME.Saturday
    Sunday = TIME.Sunday


class Greg(DefinedNamespace):
    """
    OWL-Time Gregorian Calendar
    Generated from: https://www.w3.org/ns/time/gregorian#
    """
    January: URIRef
    February: URIRef
    March: URIRef
    April: URIRef
    May: URIRef
    June: URIRef
    July: URIRef
    August: URIRef
    September: URIRef
    October: URIRef
    November: URIRef
    December: URIRef

    _NS = Namespace("http://www.w3.org/ns/time/gregorian#")


class MonthOfYear(Enum):
    January = Greg.January
    February = Greg.February
    March = Greg.March
    April = Greg.April
    May = Greg.May
    June = Greg.June
    July = Greg.July
    August = Greg.August
    September = Greg.September
    October = Greg.October
    November = Greg.November
    December = Greg.December


class GeneralDateTimeDescription(RDFModel):
    """
    Description of date and time structured with separate values for the various elements of a calendar-clock system
    """
    model_config = ConfigDict(title=TIME.GeneralDateTimeDescription)
    timeZone: AnyHttpUrl = Field(default=None,
                                 description="The time zone for clock elements in the temporal position",
                                 rdf_term=TIME.timeZone,
                                 rdf_type="uri")
    unitType: AnyHttpUrl = Field(description="The temporal unit which provides the precision of a date-time value or "
                                             "scale of a temporal extent",
                                 rdf_term=TIME.unitType,
                                 rdf_type="uri")
    hasTRS: AnyHttpUrl = Field(description="The temporal reference system used by a temporal position or extent "
                                           "description",
                               rdf_term=TIME.hasTRS,
                               rdf_type="uri"
                               )
    year: str = Field(default=None,
                      description="Year position in a calendar-clock system. The range of this property is not "
                                  "specified, so can be replaced by any specific representation of a calendar year "
                                  "from any calendar.",
                      rdf_term=TIME.year,
                      rdf_type="xsd:gYear")
    month: str = Field(default=None,
                       description="Month position in a calendar-clock system. The range of this property is not "
                                   "specified, so can be replaced by any specific representation of a calendar month "
                                   "from any calendar.",
                       rdf_term=TIME.month,
                       rdf_type="xsd:gMonth")
    day: str = Field(default=None,
                     description="Day position in a calendar-clock system. The range of this property is not "
                                 "specified, so can be replaced by any specific representation of a calendar day from "
                                 "any calendar.",
                     rdf_term=TIME.day,
                     rdf_type="xsd:gDay")
    hour: int = Field(default=None,
                      description="Hour position in a calendar-clock system",
                      ge=0,
                      rdf_term=TIME.hour,
                      rdf_type="xsd:nonNegativeInteger")
    minute: int = Field(default=None,
                        description="Minute position in a calendar-clock system",
                        ge=0,
                        rdf_term=TIME.minute,
                        rdf_type="xsd:nonNegativeInteger")
    second: float = Field(default=None,
                          description="Second position in a calendar-clock system.",
                          rdf_term=TIME.second,
                          rdf_type="xsd:decimal")
    week: int = Field(default=None,
                      description="Week number within the year.",
                      ge=0,
                      rdf_term=TIME.week,
                      rdf_type="xsd:nonNegativeInteger")
    dayOfYear: int = Field(default=None,
                           description="The number of the day within the year",
                           ge=0,
                           rdf_term=TIME.dayOfYear,
                           rdf_type="xsd:nonNegativeInteger")
    dayOfWeek: AnyHttpUrl = Field(default=None,
                                  description="The day of week, whose value is a member of the class time:DayOfWeek",
                                  rdf_term=TIME.dayOfWeek,
                                  rdf_type="uri")
    monthOfYear: AnyHttpUrl = Field(default=None,
                                    description="The month of the year, whose value is a member of the class "
                                                "time:MonthOfYear",
                                    rdf_term=TIME.monthOfYear,
                                    rdf_type="uri")


class DateTimeDescription(GeneralDateTimeDescription):
    """
    Description of date and time structured with separate values for the various elements of a calendar-clock system.
    The temporal reference system is fixed to Gregorian Calendar, and the range of year, month, day properties
    restricted to corresponding XML Schema types xsd:gYear, xsd:gMonth and xsd:gDay, respectively.
    """

    hasTRS: typing.Literal[GREG_URL] = Field(default=GREG_URL,
                                             description="The temporal reference system used by a temporal position or "
                                                         "extent description",
                                             rdf_term=TIME.hasTRS,
                                             rdf_type="uri")

    year: str = Field(default=None,
                      description="Year position in a calendar-clock system. The range of this property is not "
                                  "specified, so can be replaced by any specific representation of a calendar year "
                                  "from any calendar.",
                      pattern="-?([1-9][0-9]{3,}|0[0-9]{3})(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?",
                      rdf_term=TIME.year,
                      rdf_type="xsd:gYear")
    month: str = Field(default=None,
                       description="Month position in a calendar-clock system. The range of this property is not "
                                   "specified, so can be replaced by any specific representation of a calendar month "
                                   "from any calendar.",
                       pattern="--(0[1-9]|1[0-2])(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?",
                       rdf_term=TIME.month,
                       rdf_type="xsd:gMonth")
    day: str = Field(default=None,
                     description="Day position in a calendar-clock system. The range of this property is not "
                                 "specified, so can be replaced by any specific representation of a calendar day from "
                                 "any calendar.",
                     pattern="---(0[1-9]|[12][0-9]|3[01])(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?",
                     rdf_term=TIME.day,
                     rdf_type="xsd:gDay")

    hour: int = Field(default=None,
                      description="Hour position in a calendar-clock system",
                      le=23,
                      ge=0,
                      rdf_term=TIME.hour,
                      rdf_type="xsd:nonNegativeInteger")
    minute: int = Field(default=None,
                        description="Minute position in a calendar-clock system",
                        le=59,
                        ge=0,
                        rdf_term=TIME.minute,
                        rdf_type="xsd:nonNegativeInteger")
    second: float = Field(default=None,
                          description="Second position in a calendar-clock system.",
                          ge=0,
                          lt=60,
                          rdf_term=TIME.second,
                          rdf_type="xsd:decimal")
    week: int = Field(default=None,
                      description="Week number within the year.",
                      le=53,
                      ge=1,
                      rdf_term=TIME.week,
                      rdf_type="xsd:nonNegativeInteger")
    dayOfYear: int = Field(default=None,
                           description="The number of the day within the year",
                           ge=1,
                           le=366,
                           rdf_term=TIME.dayOfYear,
                           rdf_type="xsd:nonNegativeInteger")
    dayOfWeek: DayOfWeek = Field(default=None,
                                 description="The day of week, whose value is a member of the class time:DayOfWeek",
                                 rdf_term=TIME.dayOfWeek,
                                 rdf_type="uri")
    monthOfYear: MonthOfYear = Field(default=None,
                                     description="The month of the year, whose value is a member of the class "
                                                 "time:MonthOfYear",
                                     rdf_term=TIME.monthOfYear,
                                     rdf_type="uri")

    @field_validator("dayOfWeek", "monthOfYear", mode="before")
    @classmethod
    def force_uriref(cls, value: [str, DayOfWeek, MonthOfYear]) -> URIRef:
        """
        In case data is provided as json URIRef references are strings, they are converted to URIRef before
         type/values checks on model instantiation
        """
        if isinstance(value, str):
            return URIRef(value)
        else:
            return value

    # Some combinations of properties are redundant. For example, within a specified :year if :dayOfYear is provided 
    # then :day and :month can be computed, and vice versa. Individual values SHOULD be consistent with each other and 
    # the calendar, indicated through the value of the :hasTRS property.


class TimeInstant(RDFModel):
    """A temporal entity with zero extent or duration"""
    model_config = ConfigDict(title=TIME.Instant)

    inXSDDate: date = Field(default=None,
                            description="Position of an instant, expressed using xsd:date",
                            rdf_term=TIME.inXSDDate,
                            rdf_type="xsd:date"
                            )
    inXSDDateTime: NaiveDatetime = Field(default=None,
                                         description="(deprecated) Position of an instant, expressed using "
                                                     "xsd:dateTime",
                                         deprecated=True,
                                         rdf_term=TIME.inXSDDateTime,
                                         rdf_type="xsd:dateTime")
    inXSDDateTimeStamp: AwareDatetime = Field(default=None,
                                              description="Position of an instant, expressed using xsd:dateTimeStamp, "
                                                          "in which the time-zone field is mandatory",
                                              rdf_term=TIME.inXSDDateTimeStamp,
                                              rdf_type="xsd:dateTimeStamp"
                                              )
    inXSDgYear: str = Field(default=None,
                            description="Position of an instant, expressed using xsd:gYear",
                            pattern="-?([1-9][0-9]{3,}|0[0-9]{3})(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?",
                            rdf_term=TIME.inXSDgYear,
                            rdf_type="xsd:gYear"
                            )
    inXSDgYearMonth: str = Field(default=None,
                                 description="Position of an instant, expressed using xsd:gYearMonth",
                                 pattern="-?([1-9][0-9]{3,}|0[0-9]{3})-(0[1-9]|1[0-2])(Z|(\+|-)((0[0-9]|1[0-3]):"
                                         "[0-5][0-9]|14:00))?",
                                 rdf_term=TIME.inXSDgYearMonth,
                                 rdf_type="xsd:gYearMonth"
                                 )
    inTimePosition: TimePosition = Field(default=None,
                                         description="Position of an instant, expressed as a temporal coordinate or "
                                                     "nominal val",
                                         rdf_term=TIME.inTimePosition,
                                         rdf_type=TIME.TimePosition
                                         )
    inDateTime: GeneralDateTimeDescription = Field(default=None,
                                                   description="Position of an instant, expressed using a structured "
                                                               "description",
                                                   rdf_term=TIME.inDateTime,
                                                   rdf_type=TIME.GeneralDateTimeDescription
                                                   )

    @model_validator(mode="before")
    @classmethod
    def warn_deprecated(cls, data: Dict) -> Dict[str, Any]:
        if data.get("inXSDDateTime"):
            logger.warning("'inXSDDateTime' is deprecated, consider using `inXSDDateTimeStamp` instead")
        return data

    @model_validator(mode="before")
    @classmethod
    def validate(cls, data: Dict) -> Dict[str, Any]:
        if len(data) > 1:
            raise ValueError("'inXSDDate', 'inXSDDateTime' (deprecated), 'inXSDDateTimeStamp', 'inXSDgYear', "
                             "'inXSDgYearMonth', 'inTimePosition', and 'inDateTime' are alternative ways to describe "
                             "the temporal position of an Instant, only one should be provided")
        return data


class PeriodOfTime(RDFModel):
    model_config = ConfigDict(title=DCTERMS.PeriodOfTime)
    """
    An interval of time that is named or defined by its start and end,
    https://www.w3.org/TR/vocab-dcat-3/#Class:Period_of_Time
    """
    start_date: LiteralField = Field(default=None,
                                     description="The start of the period",
                                     rdf_term=DCAT.startDate,
                                     rdf_type="rdfs_literal")
    end_date: LiteralField = Field(default=None,
                                   description="The end of the period",
                                   rdf_term=DCAT.endDate,
                                   rdf_type="rdfs_literal")
    beginning: TimeInstant = Field(default=None,
                                   description="Beginning of a period or interval",
                                   rdf_term=TIME.hasBeginning,
                                   rdf_type=TIME.Instant)
    end: TimeInstant = Field(default=None,
                             description="End of a period or interval",
                             rdf_term=TIME.hasEnd,
                             rdf_type=TIME.Instant)

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def force_literal_field(cls, value: [str, LiteralField]) -> LiteralField:
        """
        In case value is provided as a string, convert to LiteralField object with none as datatype and language
        """
        if isinstance(value, str):
            return LiteralField(value=value)
        else:
            return value

    @model_validator(mode="before")
    @classmethod
    def validate(cls, data: Dict) -> Dict[str, Any]:
        if (data.get("start_date") and
            (data.get("beginning") or data.get("end"))
        ) or (data.get("end_date") and (data.get("end") or data.get("beginning"))):
            raise ValueError("The start and end of the interval SHOULD be given by using properties dcat:startDate "
                             "or time:hasBeginning, and dcat:endDate or time:hasEnd, respectively, see "
                             "https://www.w3.org/TR/vocab-dcat-3/#Class:Period_of_Time.")
        return data


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parent.resolve(), "json_models")
    models = ["TimePosition", "GeneralDateTimeDescription", "DateTimeDescription", "TimeInstant", "PeriodOfTime"]
    for model_name in models:
        with open(Path(json_models_folder, f"{model_name}.json"), "w") as schema_file:
            model_schema = globals()[model_name].model_json_schema()
            json.dump(model_schema, schema_file, indent=2)
