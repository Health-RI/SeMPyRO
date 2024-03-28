# Copyright 2024 Stichting Health-RI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import dateutil.parser as parser

from datetime import datetime
from pydantic import ValidationError
from typing import Union, Any

from sempyro import LiteralField
from sempyro.utils.constants import year_pattern, year_month_pattern


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
