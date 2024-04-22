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


class GeoSPARQL(DefinedNamespace):
    """
    GeoSPARQL Ontology Namespace
    Generated based on https://opengeospatial.github.io/ogc-geosparql/geosparql11/geo.ttl#
    on 07-02-2024
    """

    _NS = Namespace("http://www.opengis.net/ont/geosparql#")
    # https://opengeospatial.github.io/ogc-geosparql/geosparql11/geo.ttl#Geometry

    # http://www.w3.org/2000/01/rdf-schema#Datatype
    gmlLiteral: URIRef  # A GML serialization of a Geometry object.
    wktLiteral: URIRef  # A Well-known Text serialization of a Geometry object.
    geoJSONLiteral: URIRef  # A GeoJSON serialization of a Geometry object.
    kmlLiteral: URIRef  # A KML serialization of a Geometry object.
    dggsLiteral: URIRef  # A textual serialization of a Discrete Global Grid (DGGS) Geometry object.

    # http://www.w3.org/2002/07/owl#ObjectProperty
    defaultGeometry: URIRef  # The default Geometry to be used in spatial calculations. It is usually the most detailed Geometry.
    hasDefaultGeometry: URIRef  # The default Geometry to be used in spatial calculations. It is usually the most detailed Geometry.
    ehContains: URIRef  # States that the subject SpatialObject spatially contains the object SpatialObject. DE-9IM: T*TFF*FF*
    ehCoveredBy: URIRef  # States that the subject SpatialObject is spatially covered by the object SpatialObject. DE-9IM: TFF*TFT**
    ehCovers: URIRef  # States that the subject SpatialObject spatially covers the object SpatialObject. DE-9IM: T*TFT*FF*
    ehDisjoint: URIRef  # States that the subject SpatialObject is spatially disjoint from the object SpatialObject. DE-9IM: FF*FF****
    ehEquals: URIRef  # States that the subject SpatialObject spatially equals the object SpatialObject. DE-9IM: TFFFTFFFT
    ehInside: URIRef  # States that the subject SpatialObject is spatially inside the object SpatialObject. DE-9IM: TFF*FFT**
    ehMeet: URIRef  # States that the subject SpatialObject spatially meets the object SpatialObject. DE-9IM: FT******* ^ F**T***** ^ F***T****
    ehOverlap: URIRef  # States that the subject SpatialObject spatially overlaps the object SpatialObject. DE-9IM: T*T***T**
    hasGeometry: URIRef  # A spatial representation for a given Feature.
    hasBoundingBox: URIRef  # The minimum or smallest bounding or enclosing box of a given Feature.
    hasCentroid: URIRef  # The arithmetic mean position of all the Geometry points of a given Feature.
    hasLength: URIRef  # The length of a Spatial Object.
    hasPerimeterLength: URIRef  # The length of the perimeter of a Spatial Object.
    hasArea: URIRef  # The area of a Spatial Object.
    hasVolume: URIRef  # The volume of a three-dimensional Spatial Object.
    hasSpatialResolution: URIRef  # The spatial resolution of a Geometry.
    hasSpatialAccuracy: URIRef  # The positional accuracy of the coordinates of a Geometry.
    rcc8dc: URIRef  # States that the subject SpatialObject is spatially disjoint from the object SpatialObject. DE-9IM: FFTFFTTTT
    rcc8ec: URIRef  # States that the subject SpatialObject spatially meets the object SpatialObject. DE-9IM: FFTFTTTTT
    rcc8eq: URIRef  # States that the subject SpatialObject spatially equals the object SpatialObject. DE-9IM: TFFFTFFFT
    rcc8ntpp: URIRef  # States that the subject SpatialObject is spatially inside the object SpatialObject. DE-9IM: TFFTFFTTT
    rcc8ntppi: URIRef  # States that the subject SpatialObject spatially contains the object SpatialObject. DE-9IM: TTTFFTFFT
    rcc8po: URIRef  # States that the subject SpatialObject spatially overlaps the object SpatialObject. DE-9IM: TTTTTTTTT
    rcc8tpp: URIRef  # States that the subject SpatialObject is spatially covered by the object SpatialObject. DE-9IM: TFFTTFTTT
    rcc8tppi: URIRef  # States that the subject SpatialObject spatially covers the object SpatialObject. DE-9IM: TTTFTTFFT
    sfContains: URIRef  # States that the subject SpatialObject spatially contains the object SpatialObject. DE-9IM: T*****FF*
    sfCrosses: URIRef  # States that the subject SpatialObject spatially crosses the object SpatialObject. DE-9IM: T*T******
    sfDisjoint: URIRef  # States that the subject SpatialObject is spatially disjoint from the object SpatialObject. DE-9IM: FF*FF****
    sfEquals: URIRef  # States that the subject SpatialObject spatially equals the object SpatialObject. DE-9IM: TFFFTFFFT
    sfIntersects: URIRef  # States that the subject SpatialObject is not spatially disjoint from the object SpatialObject. DE-9IM: T******** ^ *T******* ^ ***T***** ^ ****T****
    sfOverlaps: URIRef  # States that the subject SpatialObject spatially overlaps the object SpatialObject. DE-9IM: T*T***T**
    sfTouches: URIRef  # States that the subject SpatialObject spatially touches the object SpatialObject. DE-9IM: FT******* ^ F**T***** ^ F***T****
    sfWithin: URIRef  # States that the subject SpatialObject is spatially within the object SpatialObject. DE-9IM: T*F**F***
    hasSize: URIRef  # Subproperties of this property are used to indicate the size of a Spatial Object as a measurement or estimate of one or more dimensions of the Spatial Object's spatial presence.

    # http://www.w3.org/2002/07/owl#DatatypeProperty
    asGML: URIRef  # The GML serialization of a Geometry
    asWKT: URIRef  # The WKT serialization of a Geometry
    asGeoJSON: URIRef  # The GeoJSON serialization of a Geometry
    asKML: URIRef  # The KML serialization of a Geometry
    asDGGS: URIRef  # The Discrete Global Grid System (DGGS) serialization of a Geometry
    coordinateDimension: URIRef  # The number of measurements or axes needed to describe the position of this Geometry in a coordinate system.
    dimension: URIRef  # The topological dimension of this geometric object, which must be less than or equal to the coordinate dimension. In non-homogeneous collections, this will return the largest topological dimension of the contained objects.
    hasSerialization: URIRef  # Connects a Geometry object with its text-based serialization.
    isEmpty: URIRef  # (true) if this geometric object is the empty Geometry. If true, then this geometric object represents the empty point set for the coordinate space.
    isSimple: URIRef  # (true) if this geometric object has no anomalous geometric points, such as self intersection or self tangency.
    spatialDimension: URIRef  # The number of measurements or axes needed to describe the spatial position of this Geometry in a coordinate system.
    hasMetricSpatialResolution: URIRef  # Spatial resolution specifies the level of detail of a Geometry. It the smallest dinstinguishable distance between spatially adjacent coordinates.
    hasMetricSpatialAccuracy: URIRef  # The positional accuracy of the coordinates of a Geometry in meters.
    hasMetricLength: URIRef  # The length of a Spatial Object in meters.
    hasMetricPerimeterLength: URIRef  # The length of the perimeter of a Spatial Object in meters.
    hasMetricArea: URIRef  # The area of a Spatial Object in square meters.
    hasMetricVolume: URIRef  # The volume of a Spatial Object in cubic meters.
    hasMetricSize: URIRef  # Subproperties of this property are used to indicate the size of a Spatial Object, as a measurement or estimate of one or more dimensions of the Spatial Object's spatial presence. Units are always metric (meter, square meter or cubic meter).

    # # http://www.w3.org/2002/07/owl#Class
    Feature: URIRef  # A discrete spatial phenomenon in a universe of discourse.
    FeatureCollection: URIRef  # A collection of individual Features.
    Geometry: URIRef  # A coherent set of direct positions in space. The positions are held within a Spatial Reference System (SRS).
    GeometryCollection: URIRef  # A collection of individual Geometries.
    SpatialObject: URIRef  # Anything spatial (being or having a shape, position or an extent).
    SpatialObjectCollection: URIRef  # A collection of individual Spatial Objects.
