from typing import List, Union, Any
from pydantic import Field, AnyHttpUrl
from rdflib import Namespace, URIRef
from rdflib.namespace import DCAT, DCTERMS, DefinedNamespace, PROV

from dcat.dcat_resource import DCATResource, LiteralField
from dcat.dcat_time_models import PeriodOfTime
from dcat.rdf_model import RDFModel

from enum import Enum

from namespaces.DCATv3 import DCATv3
from namespaces.LOCN import LOCN


class DatasetSeries(DCATResource):
    pass


class Geometry(RDFModel):
    pass


# Implementations shall allow the properties geo:dimension, geo:coordinateDimension, geo:spatialDimension, geo:hasSpatialResolution, geo:hasMetricSpatialResolution, geo:hasSpatialAccuracy, geo:hasMetricSpatialAccuracy, geo:isEmpty, geo:isSimple and geo:hasSerialization to be used in SPARQL graph patterns.
# https://docs.ogc.org/is/22-047r1/22-047r1.html#_class_geogeometry
# https://opengeospatial.github.io/ogc-geosparql/geosparql11/geo.ttl#


class Activity(RDFModel):
    pass


class Location(RDFModel):
    geometry: Union[LiteralField, Geometry] = Field(
        default=None,
        description="Associates a spatial thing [SDW-BP] with a corresponding geometry.",
        rdf_term=LOCN.geometry,
        rdf_type="geosparql:wktLiteral"
    )  # todo datatype
    bounding_box: Any = Field(
        default=None,
        description="The geographic bounding box of a spatial thing [SDW-BP].",
        rdf_term=DCAT.bbox,
        rdf_type="rdf_literal"
    )
    centroid: Any = Field(default=None,
                          description="The geographic center (centroid) of a spatial thing [SDW-BP].",
                          rdf_term=DCAT.centroid,
                          rdf_type="rdf_literal"
                          )


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


class Frequency(Enum):
    triennial = FREQ.triennial
    biennial = FREQ.biennial
    annual = FREQ.annual
    semiannual = FREQ.semiannual
    threeTimesAYear = FREQ.threeTimesAYear
    quarterly = FREQ.quarterly
    bimonthly = FREQ.bimonthly
    monthly = FREQ.monthly
    semimonthly = FREQ.semimonthly
    biweekly = FREQ.biweekly
    threeTimesAMonth = FREQ.threeTimesAMonth
    weekly = FREQ.weekly
    semiweekly = FREQ.semiweekly
    threeTimesAWeek = FREQ.threeTimesAWeek
    daily = FREQ.daily
    continuous = FREQ.continuous
    irregular = FREQ.irregular


class DCATDataset(DCATResource):
    distribution: List[AnyHttpUrl] = Field(
        default=None,
        description="An available distribution of the dataset.",
        rdf_term=DCAT.distribution,
        rdf_type="uri"
    )
    temporal_coverage: List[PeriodOfTime] = Field(
        default=None,
        description="The temporal period that the dataset covers.",
        rdf_term=DCTERMS.temporal,
        rdf_type=PeriodOfTime
    )
    frequency: Union[AnyHttpUrl, Frequency] = Field(
        default=None,
        description="The frequency at which a dataset is published.",
        rfd_term=DCTERMS.accrualPeriodicity,
        rdf_type="uri"
    )
    in_series: List[AnyHttpUrl] = Field(
        default=None,
        description="A dataset series of which the dataset is part.",
        rdf_term=DCATv3.inSeries,
        rdf_type="uri"
    )
    spatial: List[Union[AnyHttpUrl, Location]] = Field(
        default=None,
        description="The geographical area covered by the dataset.",
        alias="geographical_coverage",
        rdf_term=DCTERMS.spatial,
        rdf_type="uri")

    spatial_resolution: List[float] = Field(
        default=None,
        description="Minimum spatial separation resolvable in a dataset, "
                    "measured in meters.",
        rdf_term=DCAT.spatialResolutionInMeters,
        rdf_type="xsd:decimal")

    temporal_resolution: List[str] = Field(
        default=None,
        description="Minimum time period resolvable in the dataset.",
        rdf_term=DCAT.spatialResolutionInMeters,
        rdf_type="xsd:duration"
    )

    was_generated_by: List[Activity] = Field(
        default=None,
        description="An activity that generated, or provides the business context for, the creation of the dataset.",
        rdf_term=PROV.wasGeneratedBy,
        rdf_type="uri"
    )
