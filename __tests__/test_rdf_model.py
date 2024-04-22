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

from datetime import date, datetime
from typing import Union

import pytest
from pydantic import AwareDatetime, NaiveDatetime, field_validator
from rdflib import XSD, Graph, Literal, URIRef
from rdflib.compare import to_isomorphic

from sempyro import RDFModel
from sempyro.dcat import DCATDataset
from sempyro.utils.validator_functions import date_handler


@pytest.mark.parametrize("date_input,output", [
    ("1992", Literal("1992", datatype=XSD.gYear),),
    (1707995797, Literal("2024-02-15T11:16:37+00:00", datatype=XSD.dateTime)),
    ("November 9, 1999", Literal("1999-11-09T00:00:00", datatype=XSD.dateTime)),
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


@pytest.mark.parametrize("issued,expected_date",
                         [
                             ("1992", '"1992"^^xsd:gYear'),
                             ("November 9, 1999", '"1999-11-09T00:00:00"^^xsd:dateTime'),
                             ("2006-09", '"2006-09"^^xsd:gYearMonth'),
                             ("25-05-1998", '"1998-05-25T00:00:00"^^xsd:dateTime'),
                             (datetime.now().date(), f'"{datetime.now().date()!s}"^^xsd:date')
                         ]
                         )
def test_time_serialization(issued, expected_date):
    title = ["Test title"]
    description = ["Test description"]
    expected = (f"@prefix dcat: <http://www.w3.org/ns/dcat#> .\n"
                f"@prefix dcterms: <http://purl.org/dc/terms/> .\n"
                f"@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n"
                f"<http://example.com/1> a dcat:Dataset ;\n"
                f'dcterms:description "Test description" ;\n'
                f"dcterms:issued {expected_date} ;\n"
                f'dcterms:title "Test title" .\n')
    dataset = DCATDataset(title=title,
                          description=description,
                          release_date=issued
                          )
    actual = dataset.to_graph(URIRef("http://example.com/1"))
    expected = Graph().parse(data=expected, format="ttl")
    assert to_isomorphic(actual) == to_isomorphic(expected)
