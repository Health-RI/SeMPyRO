from abc import ABCMeta
import logging
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from rdflib import DCAT, DCTERMS, Dataset
from typing import List, Optional, Union
from pydantic import BaseModel, Field, validator, AwareDatetime, NaiveDatetime
from rdflib import BNode, Graph, Namespace, URIRef, Literal
from rdflib.namespace import DCAT, DCTERMS, RDF, XSD, RDFS, TIME

from dcat.dcat_resource import Temporal, DCATResource

import ruamel.yaml
import json

from enum import Enum

from datetime import date, datetime, time

from dcat.DCATv3 import DCATv3

VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")

RDF_KEY = "rdf_term"
RDF_TYPE_KEY = "rdf_type"


class DatasetSeries(DCATResource):
    pass


# DCTERMS.Frequency


class DCATDataset(DCATResource):
    distribution: List[URIRef] = Field(default=None,
                                       description="An available distribution of the dataset.",
                                       rdf_term=DCAT.distribution)

    temporal_coverage: Temporal = Field(default=None,
                                        description="The temporal period that the dataset covers.",
                                        rdf_term=DCTERMS.temporal)  # DCTERMS.temporal, node_type=DCTERMS.PeriodOfTime

    frequency: str = Field(default=None,
                           description="The frequency at which a dataset is published.",
                           rfd_term=DCTERMS.accrualPeriodicity,
                           rdf_type="uri"),  # todo enum

    in_series: object = Field(default=None,
                              description="A dataset series of which the dataset is part.")

    spatial: List[Union[str, object]] = Field(default=None,
                                              description="The geographical area covered by the dataset.",
                                              rdf_type="uri")  # dcterms:Location

    spatial_resolution: float = Field(default=None,
                                      description="Minimum spatial separation resolvable in a dataset, "
                                                  "measured in meters.",
                                      rdf_term=DCAT.spatialResolutionInMeters,
                                      rdf_type="literal")  # xsd:decimal

    temporal_resolution: str = Field(default=None,
                                     description="Minimum time period resolvable in the dataset.",
                                     rdf_term=DCAT.spatialResolutionInMeters,
                                     rdf_type="literal"
                                     )  # xsd:duration

    was_generated_by: str = Field(default=None,
                                  description="An activity that generated, or provides the business context for, "
                                              "the creation of the dataset.",
                                  )  # https://www.w3.org/TR/prov-o/#Activity
