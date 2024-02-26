from datetime import datetime
import dateutil.parser as parser
from pydantic import ValidationError
import re
from typing import Union, Any

from dcat.rdf_model import LiteralField
from utils.constants import year_pattern, year_month_pattern


def force_literal_field(value: Union[str, LiteralField]) -> LiteralField:
    """
    Converts string values to LiteralField object with none as datatype and language
    :param value: input value
    :param datatype: Optional URIRef
    :return: LiteralField
    """
    if isinstance(value, str):
        value = LiteralField(value=value)
    return value


def date_handler(value: Union[str, Any]) -> Union[str, datetime, Any]:
    """
    Checks if a string input matches xsd:gYear or xsd:gYearMonth, or can be parsed to a datetime
    :param value: str, input value
    :return: a string if input matches xsd:gYear or xsd:gYearMonth or a :class:`datetime.datetime` object, 
    non-string inputs are returned unchanged
    :raises: pydantic.ValidationError in case a string can not be parsed to datetime.datetime
    """
    if isinstance(value, str):
        if not (re.match(year_pattern, value) or re.match(year_month_pattern, value)):
            try:
                value = parser.parse(value)
            except TypeError:
                raise ValidationError
    return value
