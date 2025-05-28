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
from datetime import datetime
from typing import Any, Union, List

from dateutil import parser
from pydantic import ValidationError, AnyUrl
from pydantic.networks import validate_email

from sempyro import LiteralField
from sempyro.utils.constants import year_month_pattern, year_pattern


def convert_to_literal(value: Union[List[Union[str, LiteralField]], Union[str, LiteralField]]
                       ) -> Union[Union[LiteralField, List[LiteralField]], None]:
    if not value:
        return None
    if isinstance(value, list):
        return [force_literal_field(item) for item in value]
    return force_literal_field(value)


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


def convert_to_mailto(value: str) -> AnyUrl:
    """
    Checks if a string starts with `mailto:`, and if not, prefixes it with this. After that it uses a
    `validate_email` from Pydantic to validate the email.
    :param value: str, input value
    :return: a variable of type `AnyUrl` containing a valid email address with the `mailto:` prefix.
    :raises: PydanticCustomError in case the email is not valid.
    """
    mail_part = value
    if value.startswith("mailto:"):
        mail_part = re.split(r":|//", value)[-1]
    mail_part = validate_email(mail_part)[1]
    return AnyUrl(f"mailto:{mail_part}")


def validate_convert_email(value: Union[str, None, AnyUrl, List[Union[str, AnyUrl]]]) -> Union[None, List[AnyUrl], AnyUrl]:
    """
    Iteratively applies the function `convert_to_mailto` over the (list of) input value(s).
    :param value: list or str, (list of) input value(s)
    :return: a list of validated emails with the `mailto:` prefix.
    """
    if isinstance(value, list) and value[0]:
        return [convert_to_mailto(item) for item in value]
    elif value:
        return convert_to_mailto(str(value))
    else:
        return None
