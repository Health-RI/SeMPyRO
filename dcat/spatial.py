from pydantic import AnyHttpUrl, ConfigDict, Field
from rdflib import DCAT, DCTERMS
from typing import Any, AnyStr, Union

from dcat.rdf_model import RDFModel, LiteralField

from namespaces.GEOSPARQL import GeoSPARQL
from namespaces.LOCN import LOCN


class Geometry(RDFModel):
    """
    Geometry class for GeoSPARQL Geometry specification
    https://docs.ogc.org/is/22-047r1/22-047r1.html#_class_geogeometry
    https://opengeospatial.github.io/ogc-geosparql/geosparql11/geo.ttl#
    """
    model_config = ConfigDict(title=GeoSPARQL.Geometry)

    dimension: int = Field(
        default=None,
        description="The topological dimension of this geometric object, which must be less than or equal to the "
                    "coordinate dimension. In non-homogeneous collections, this is the largest topological dimension "
                    "of the contained objects.",
        rdf_term=GeoSPARQL.dimension,
        rdf_type="xsd:integer"
    )
    coordinateDimension: int = Field(
        default=None,
        description="The number of measurements or axes needed to describe the position of this Geometry in a "
                    "coordinate system.",
        rdf_term=GeoSPARQL.coordinateDimension,
        rdf_type="xsd:integer"
    )
    spatialDimension: int = Field(
        default=None,
        description="The number of measurements or axes needed to describe the spatial position of this Geometry in "
                    "a coordinate system.",
        rdf_term=GeoSPARQL.spatialDimension,
        rdf_type="xsd:integer"
    )
    hasSpatialResolution: AnyHttpUrl = Field(
        default=None,
        description="The spatial resolution of a Geometry",
        rdf_term=GeoSPARQL.hasSpatialResolution,
        rdf_type="uri"
    )
    hasMetricSpatialResolution: float = Field(
        default=None,
        description="The spatial resolution of a Geometry in meters.",
        rdf_term=GeoSPARQL.hasMetricSpatialResolution,
        rdf_type="xsd:double"
    )
    hasSpatialAccuracy: Any = Field(
        default=None,
        description="The positional accuracy of the coordinates of a Geometry",
        rdf_term=GeoSPARQL.hasSpatialAccuracy,
        rdf_type="uri"
    )
    hasMetricSpatialAccuracy: float = Field(
        default=None,
        description="The positional accuracy of the coordinates of a Geometry in meters.",
        rdf_term=GeoSPARQL.hasMetricSpatialAccuracy,
        rdf_type="xsd:double"
    )
    isEmpty: bool = Field(
        default=None,
        description="(true) if this geometric object is the empty Geometry. If true, then this geometric object "
                    "represents the empty point set for the coordinate space.",
        rdf_term=GeoSPARQL.isEmpty,
        rdf_type="xsd:boolean"
    )
    isSimple: bool = Field(
        default=None,
        description="(true) if this geometric object has no anomalous geometric points, such as self intersection or "
                    "self tangency.",
        rdf_term=GeoSPARQL.isSimple,
        rdf_type="xsd:boolean"
    )
    hasSerialization: Union[str, LiteralField] = Field(
        default=None,
        description="Connects a Geometry object with its text-based serialization.",
        rdf_term=GeoSPARQL.hasSerialization,
        rdf_type="rdfs_literal"
    )


class Location(RDFModel):
    model_config = ConfigDict(title=DCTERMS.Location)

    geometry: Union[LiteralField, Geometry, Any] = Field(
        default=None,
        description="Associates a spatial thing [SDW-BP] with a corresponding geometry.",
        rdf_term=LOCN.geometry,
        rdf_type="geosparql:wktLiteral"
    )  # todo datatype
    bounding_box: Union[LiteralField, AnyStr] = Field(
        default=None,
        description="The geographic bounding box of a spatial thing [SDW-BP].",
        rdf_term=DCAT.bbox,
        rdf_type="rdf_literal"
    )
    centroid: Any = Field(
        default=None,
        description="The geographic center (centroid) of a spatial thing [SDW-BP].",
        rdf_term=DCAT.centroid,
        rdf_type="rdf_literal"
    )
