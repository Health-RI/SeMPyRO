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

from sempyro import RDFModel
from datetime import date, datetime
from pydantic import AwareDatetime, NaiveDatetime, field_validator
from rdflib import Literal, XSD
import pytest
from typing import Union
from sempyro.utils.validator_functions import date_handler


@pytest.mark.parametrize("date_input,output", [
    ("1992", Literal("1992", datatype=XSD.gYear),),
    (1707995797, Literal("2024-02-15 11:16:37+00:00", datatype=XSD.dateTime)),
    ("November 9, 1999", Literal("1999-11-09 00:00:00", datatype=XSD.dateTime)),
    (datetime.date(datetime.now()), Literal(str(datetime.now().date()), datatype=XSD.date)),
    ("2006-09", Literal("2006-09", datatype=XSD.gYearMonth))
])
def test_time_literal(date_input, output):
    class myModel(RDFModel):
        date_field: Union[str, datetime, date, AwareDatetime, NaiveDatetime]

        @field_validator("date_field", mode="before")
        @classmethod
        def date_validator(cls, value):
            return date_handler(value)

    obj = myModel(date_field=date_input)
    expected = obj._convert_to_datetime_literal(obj.date_field)
    assert expected == output
