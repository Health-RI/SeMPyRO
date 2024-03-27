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

from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace


class FREQ(DefinedNamespace):
    """
    The Collection Description Frequency Namespace
    modified on 2013-05-10

    Generated based on https://www.dublincore.org/specifications/dublin-core/collection-description/frequency/freq.rdf
    """

    triennial: URIRef  # The event occurs every three years.
    biennial: URIRef  # The event occurs every two years.
    annual: URIRef  # The event occurs once a year.
    semiannual: URIRef  # The event occurs twice a year.
    threeTimesAYear: URIRef  # # The event occurs three times a year.
    quarterly: URIRef  # The event occurs every three months.
    bimonthly: URIRef  # The event occurs every two months.
    monthly: URIRef  # The event occurs once a month.
    semimonthly: URIRef  # The event occurs twice a month.
    biweekly: URIRef  # The event occurs every two weeks.
    threeTimesAMonth: URIRef  # The event occurs three times a month.
    weekly: URIRef  # The event occurs once a week.
    semiweekly: URIRef  # The event occurs twice a week.
    threeTimesAWeek: URIRef  # The event occurs three times a week.
    daily: URIRef  # The event occurs once a day.
    continuous: URIRef  # The event repeats without interruption.
    irregular: URIRef  # The event occurs at uneven intervals.

    _NS = Namespace("http://purl.org/cld/freq/")
