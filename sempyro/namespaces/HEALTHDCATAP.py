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


class HEALTHDCATAP(DefinedNamespace):
    """
    Namespace for the HealthDCAT-AP

    HealthDCAT-AP is a health-related extension of the DCAT application profile for sharing information about Catalogues
    containing Datasets and Data Services descriptions in Europe (DCAT-AP) [DCAT-AP]. DCAT-AP is maintained by the SEMIC action,
    Interoperable Europe. While DCAT-AP provides a minimal common basis within Europe to share Datasets and Data Services
    cross-border and cross-domain, HealthDCAT-AP introduces a refined RDF vocabulary to accommodate the unique requirements of electronic health data.
    The Regulation on the European Health Data Space [OJ L, 2025/327, 5.3.2025], aims to establish a unified framework
    to facilitate the sharing and exchange of electronic health data across Europe. It aligns with European standards
    for data privacy and security and specifically addresses the challenges and obstacles for the secondary use of
    health data—data repurposed from its original collection for research, innovation, or policymaking – in Europe by
    outlining specific rules and processes for data availability, usage conditions, and supporting these efforts through
    a common European infrastructure, healthdata@EU. Key articles within the Regulation detail operational mandates:
    Article 51 identifies the types of health data that must be made available for secondary use; Article 79 tasks
    the European Commission to develop an EU dataset catalogue, federating the catalogues of Member states and other
    authorised participants into HealthData@EU; and Article 77 commissions health data access bodies to provide
    metadata about available datasets, detailing their source, scope, main characteristics, data nature, and access
    conditions. The development of a healthDCAT application profile, as an extension of the DCAT application profile,
    aims to standardise health metadata within the scope of EHDS, fostering greater interoperability, findability and
    accessibility of electronic health data across the EU.

    Generated based on https://healthdcat-ap.github.io/
    Date: 2025-05-12
    """
    analytics: URIRef
    hasCodeValues: URIRef
    hasCodingSystem: URIRef
    healthTheme: URIRef
    maxTypicalAge: URIRef
    minTypicalAge: URIRef
    numberOfRecords: URIRef
    numberOfUniqueIndividuals: URIRef
    populationCoverage: URIRef
    publisherType: URIRef
    publisherNote: URIRef
    retentionPeriod: URIRef

    _NS = Namespace("http://healthdataportal.eu/ns/health#")


