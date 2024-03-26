from sempyro.rdf_model import RDFModel
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
