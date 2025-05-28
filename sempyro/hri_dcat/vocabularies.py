# Copyright 2025 Stichting Health-RI
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

from enum import Enum

from rdflib import URIRef


class GeonovumLicences(Enum):
    cc0 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/cc0")
    cc_by_10 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding10")
    cc_by_20 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding20")
    cc_by_30 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding30")
    cc_by_40 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding40")
    cc_bynd_10 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding_geen_afgeleide_werken10")
    cc_bynd_20 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding_geen_afgeleide_werken20")
    cc_bynd_30 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding_geen_afgeleide_werken30")
    cc_bynd_40 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding_geen_afgeleide_werken40")
    cc_bysa_10 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding_gelijkdelen10")
    cc_bysa_20 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding_gelijkdelen20")
    cc_bysa_30 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding_gelijkdelen30")
    cc_bysa_40 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding_gelijkdelen40")
    cc_bync_10 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding_niet_commercieel10")
    cc_bync_20 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding_niet_commercieel20")
    cc_bync_30 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding_niet_commercieel30")
    cc_bync_40 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding_niet_commercieel40")
    cc_byncnd_10 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding_niet_commercieel_geen_afgeleide_werken10")
    cc_byncnd_20 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding_niet_commercieel_geen_afgeleide_werken20")
    cc_byncnd_30 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding_niet_commercieel_geen_afgeleide_werken30")
    cc_byncnd_40 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding_niet_commercieel_geen_afgeleide_werken40")
    cc_byncsa_10 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding_niet_commercieel_gelijk_delen10")
    cc_byncsa_20 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding_niet_commercieel_gelijk_delen20")
    cc_byncsa_30 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding_niet_commercieel_gelijk_delen30")
    cc_byncsa_40 = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/naamsvermelding_niet_commercieel_gelijk_delen40")
    niet_open = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/niet_open")
    public_domain_mark = URIRef("https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties/public_domain_mark")


class DatasetTheme(Enum):
    agri = URIRef("http://publications.europa.eu/resource/authority/data-theme/AGRI")
    econ = URIRef("http://publications.europa.eu/resource/authority/data-theme/ECON")
    educ = URIRef("http://publications.europa.eu/resource/authority/data-theme/EDUC")
    ener = URIRef("http://publications.europa.eu/resource/authority/data-theme/ENER")
    envi = URIRef("http://publications.europa.eu/resource/authority/data-theme/ENVI")
    gove = URIRef("http://publications.europa.eu/resource/authority/data-theme/GOVE")
    heal = URIRef("http://publications.europa.eu/resource/authority/data-theme/HEAL")
    intr = URIRef("http://publications.europa.eu/resource/authority/data-theme/INTR")
    just = URIRef("http://publications.europa.eu/resource/authority/data-theme/JUST")
    op_datpro = URIRef("http://publications.europa.eu/resource/authority/data-theme/OP_DATPRO")
    regi = URIRef("http://publications.europa.eu/resource/authority/data-theme/REGI")
    soci = URIRef("http://publications.europa.eu/resource/authority/data-theme/SOCI")
    tech = URIRef("http://publications.europa.eu/resource/authority/data-theme/TECH")
    tran = URIRef("http://publications.europa.eu/resource/authority/data-theme/TRAN")


class DatasetStatus(Enum):
    develop = URIRef("http://publications.europa.eu/resource/authority/dataset-status/DEVELOP")
    completed = URIRef("http://publications.europa.eu/resource/authority/dataset-status/COMPLETED")
    deprecated = URIRef("http://publications.europa.eu/resource/authority/dataset-status/DEPRECATED")
    withdrawn = URIRef("http://publications.europa.eu/resource/authority/dataset-status/WITHDRAWN")
    op_datpro = URIRef("http://publications.europa.eu/resource/authority/dataset-status/OP_DATPRO")
    discontinued = URIRef("http://publications.europa.eu/resource/authority/dataset-status/DISCONT")


class DistributionStatus(Enum):
    develop = URIRef("http://publications.europa.eu/resource/authority/distribution-status/DEVELOP")
    completed = URIRef("http://publications.europa.eu/resource/authority/distribution-status/COMPLETED")
    deprecated = URIRef("http://publications.europa.eu/resource/authority/distribution-status/DEPRECATED")
    withdrawn = URIRef("http://publications.europa.eu/resource/authority/distribution-status/WITHDRAWN")
    op_datpro = URIRef("http://publications.europa.eu/resource/authority/distribution-status/OP_DATPRO")
