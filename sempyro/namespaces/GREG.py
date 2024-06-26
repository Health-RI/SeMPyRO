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

from rdflib import Namespace, URIRef
from rdflib.namespace import DefinedNamespace


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
