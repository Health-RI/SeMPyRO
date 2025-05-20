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


class DCATAPv3(DefinedNamespace):
    """
    Namespace for the European DCAT-AP version 3.0.0.

    DCAT-AP is a DCAT profile for sharing information about Catalogues containing Datasets and Data Services
    descriptions in Europe, under maintenance by the SEMIC action, Interoperable Europe.
    This Application Profile provides a minimal common basis within Europe to share Datasets and Data Services
    cross-border and cross-domain.

    Generated based on https://github.com/SEMICeu/DCAT-AP/blob/3.0.0/releases/3.0.0/shacl/dcat-ap-SHACL.ttl
    Date: 2025-04-30
    """

    applicableLegislation: URIRef # The legislation that is applicable to this resource.
    availability: URIRef # An indication how long it is planned to keep the Distribution of the Dataset available.
    hvdCategory: URIRef # A data category defined in the High Value Dataset Implementing Regulation.

    _NS = Namespace("http://data.europa.eu/r5r/")
