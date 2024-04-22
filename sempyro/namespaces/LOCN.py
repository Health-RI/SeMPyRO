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


class LOCN(DefinedNamespace):
    """
    ISA Location Core Vocabulary Namespace
    Generated based on https://semiceu.github.io/Core-Location-Vocabulary/releases/w3c/locn.ttl
    on 06-02-2024
    """
    # http://www.w3.org/2002/07/owl#ObjectProperty
    address: URIRef  # The locn:address property relationship associates any resource with the locn:Address class
    addressArea: URIRef  # The name or names of a geographic area or locality that groups a number of addressable objects for addressing purposes, without being an administrative unit. This would typically be part of a city, a neighbourhood or village.
    addressId: URIRef  # The concept of adding a globally unique identifier for each instance of an address is a crucial part of the INSPIRE data spec.
    adminUnitL1: URIRef  # Best practice is to use the ISO 3166-1 code but if this is inappropriate for the context, country names should be provided in a consistent manner to reduce ambiguity. For example, either write 'United Kingdom' or 'UK' consistently throughout the data set and avoid mixing the two.
    adminUnitL2: URIRef  # The region of the address, usually a county, state or other such area that typically encompasses several localities. The domain of  locn:adminUnitL2 is locn:Address and the range is a literal, conceptually defined by the INSPIRE Geographical Name data type.
    fullAddress: URIRef  # The complete address written as a string, with or without formatting.
    geographicName: URIRef  # A geographic name is a proper noun applied to a spatial object.
    geometry: URIRef  # Associates any resource with the corresponding geometry.
    location: URIRef  # The location property links any resource to the Location Class. Asserting the location relationship implies only that the domain has some connection to a Location in time or space. It does not imply that the resource is necessarily at that location at the time when the assertion is made.
    locatorDesignator: URIRef  # A number or a sequence of characters that uniquely identifies the locator within the relevant scope(s). The full identification of the locator could include one or more locator designators.
    locatorName: URIRef  # Proper noun(s) applied to the real world entity identified by the locator. The locator name could be the name of the property or complex, of the building or part of the building, or it could be the name of a room inside a building.
    poBox: URIRef  # The Post Office Box number.
    postCode: URIRef  # The post code (a.k.a postal code, zip code etc.). Post codes are common elements in many countries' postal address systems. The domain of locn:postCode is locn:Address.
    postName: URIRef  # The key postal division of the address, usually the city. (INSPIRE's definition is "One or more names created and maintained for postal purposes to identify a subdivision of addresses and postal delivery points.").
    thoroughfare: URIRef  # An address component that represents the name of a passage or way through from one location to another. A thoroughfare is not necessarily a road, it might be a waterway or some other feature.

    # http://www.w3.org/2002/07/owl#Class
    Address: URIRef  # An "address representation" as conceptually defined by the INSPIRE Address Representation data type. The locn:addressId property may be used to link this locn:Address to other representations.
    Geometry: URIRef  # The locn:Geometry class provides the means to identify a location as a point, line, polygon, etc. expressed using coordinates in some coordinate reference system.

    _NS = Namespace("http://www.w3.org/ns/locn#")
