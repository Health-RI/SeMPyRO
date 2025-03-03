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

from pathlib import Path
from typing import Union

from pydantic import AnyHttpUrl, ConfigDict, Field, field_validator
from rdflib import DCAT, DCTERMS

from sempyro import LiteralField, RDFModel
from sempyro.namespaces import LOCN, GeoSPARQL
from sempyro.utils.validator_functions import force_literal_field


class Geometry(RDFModel):
    """
    Geometry class for GeoSPARQL Geometry specification
    """
    model_config = ConfigDict(
                              json_schema_extra={
                                  "$ontology": "https://docs.ogc.org/is/22-047r1/22-047r1.html",
                                  "$namespace": str(GeoSPARQL),
                                  "$IRI": GeoSPARQL.Geometry,
                                  "$prefix": "geo"
                              }
                              )

    dimension: int = Field(
        default=None,
        description="The topological dimension of this geometric object, which must be less than or equal to the "
                    "coordinate dimension. In non-homogeneous collections, this is the largest topological dimension "
                    "of the contained objects.",
        json_schema_extra={
            "rdf_term": GeoSPARQL.dimension,
            "rdf_type": "xsd:integer"
        }
    )
    coordinateDimension: int = Field(
        default=None,
        description="The number of measurements or axes needed to describe the position of this Geometry in a "
                    "coordinate system.",
        json_schema_extra={
            "rdf_term": GeoSPARQL.coordinateDimension,
            "rdf_type": "xsd:integer"
        }
    )
    spatialDimension: int = Field(
        default=None,
        description="The number of measurements or axes needed to describe the spatial position of this Geometry in "
                    "a coordinate system.",
        json_schema_extra={
            "rdf_term": GeoSPARQL.spatialDimension,
            "rdf_type": "xsd:integer"
        }
    )
    hasSpatialResolution: AnyHttpUrl = Field(
        default=None,
        description="The spatial resolution of a Geometry",
        json_schema_extra={
            "rdf_term": GeoSPARQL.hasSpatialResolution,
            "rdf_type": "uri"
        }
    )
    hasMetricSpatialResolution: float = Field(
        default=None,
        description="The spatial resolution of a Geometry in meters.",
        json_schema_extra={
            "rdf_term": GeoSPARQL.hasMetricSpatialResolution,
            "rdf_type": "xsd:double"
        }
    )
    hasSpatialAccuracy: AnyHttpUrl = Field(
        default=None,
        description="The positional accuracy of the coordinates of a Geometry",
        json_schema_extra={
            "rdf_term": GeoSPARQL.hasSpatialAccuracy,
            "rdf_type": "uri"
        }
    )
    hasMetricSpatialAccuracy: float = Field(
        default=None,
        description="The positional accuracy of the coordinates of a Geometry in meters.",
        json_schema_extra={
            "rdf_term": GeoSPARQL.hasMetricSpatialAccuracy,
            "rdf_type": "xsd:double"
        }
    )
    isEmpty: bool = Field(
        default=None,
        description="(true) if this geometric object is the empty Geometry. If true, then this geometric object "
                    "represents the empty point set for the coordinate space.",
        json_schema_extra={
            "rdf_term": GeoSPARQL.isEmpty,
            "rdf_type": "xsd:boolean"
        }
    )
    isSimple: bool = Field(
        default=None,
        description="(true) if this geometric object has no anomalous geometric points, such as self intersection or "
                    "self tangency.",
        json_schema_extra={
            "rdf_term": GeoSPARQL.isSimple,
            "rdf_type": "xsd:boolean"
        }
    )
    hasSerialization: Union[str, LiteralField] = Field(
        default=None,
        description="Connects a Geometry object with its text-based serialization.",
        json_schema_extra={
            "rdf_term": GeoSPARQL.hasSerialization,
            "rdf_type": "rdfs_literal"
        }
    )


class Location(RDFModel):
    """A spatial region or named place."""
    model_config = ConfigDict(title=DCTERMS.Location,
                              json_schema_extra={
                                  "$ontology": "https://www.w3.org/TR/vocab-dcat-3/",
                                  "$namespace": str(DCTERMS),
                                  "$IRI": DCTERMS.Location,
                                  "$prefix": "dcterms"
                              }
                              )

    geometry: Union[LiteralField, Geometry] = Field(
        default=None,
        description="Associates a spatial thing [SDW-BP] with a corresponding geometry.",
        # bind_namespace=("locn", str(LOCN)),
        json_schema_extra={
            "rdf_term": LOCN.geometry,
            "rdf_type": "geosparql:wktLiteral",
            "bind_namespace": ("locn", str(LOCN)),
        }
    )
    bounding_box: Union[LiteralField, str] = Field(
        default=None,
        description="The geographic bounding box of a spatial thing [SDW-BP].",
        json_schema_extra={
            "rdf_term": DCAT.bbox,
            "rdf_type": "rdfs_literal"
        }
    )
    centroid: LiteralField = Field(
        default=None,
        description="The geographic center (centroid) of a spatial thing [SDW-BP].",
        json_schema_extra={
            "rdf_term": DCAT.centroid,
            "rdf_type": "geosparql:wktLiteral"
        }
    )

    @field_validator("geometry", "centroid", mode="before")
    @classmethod
    def convert_to_literal(cls, value: Union[str, LiteralField]) -> LiteralField:
        return force_literal_field(value)


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "geo")
    models = ["Geometry", "Location"]
    for model_name in models:
        model = globals()[model_name]
        model.save_schema_to_file(path=Path(json_models_folder, f"{model_name}.json"),
                                  file_format="json")
        model.save_schema_to_file(path=Path(json_models_folder, f"{model_name}.yaml"),
                                  file_format="yaml")
