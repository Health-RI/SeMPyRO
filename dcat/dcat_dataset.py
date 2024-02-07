from typing import List, Union, Any
from pydantic import Field, AnyHttpUrl, ConfigDict
from rdflib.namespace import DCAT, DCTERMS, DefinedNamespace, PROV, XSD

from dcat.dcat_resource import DCATResource, LiteralField
from dcat.dcat_time_models import PeriodOfTime
from dcat.dataset_series import DatasetSeries
from dcat.spatial import Location
from dcat.prov_classes import Activity

from enum import Enum

from namespaces.DCATv3 import DCATv3
from namespaces.FREQ import FREQ


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
    model_config = ConfigDict(title=DCAT.Dataset)

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
    in_series: List[AnyHttpUrl, DatasetSeries] = Field(
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
