# HRI Pydantic Models

**Table of content:**

- [Types of objects the package includes](#types-of-objects-the-package-includes)
  - [Available model classes](#model-classes)
  - [Namespaces](#namespaces)
  - [Enum classes](#enum-classes)
- [How a model is defined](#how-a-model-is-defined)
- [Defining a model of your own and extending models](#defining-a-model-of-your-own-and-extending-models)
- [Usage examples](#usage-examples)

## Types of objects the package includes

The package comprises three types of classes to implement DCAT model: Pydantic-based model classes, RDF namespaces and
`enum` classes.

### Model classes

All the model classes are inherited from `RDFModel` which is, in its turn, a subclass of `pydantic.BaseModel`.
They are developed to implement DCAT-AP v3 model and provide validations.

Following DCAT classes are available in the package:

- DCATResource is an abstract class corresponding [DCAT Resource](https://www.w3.org/TR/vocab-dcat-3/#Class:Resource) definition.
- DCATDataset - a subclass of DCATResource, corresponds [DCAT Dataset](https://www.w3.org/TR/vocab-dcat-3/#Class:Dataset).
- DCATCatalog - a subclass of DCATDataset, corresponds [DCAT Catalog](https://www.w3.org/TR/vocab-dcat-3/#Class:Catalog_Record).
- DatasetSeries - a subclass of DCATDataset, corresponds [DCAT Dataset Series](https://www.w3.org/TR/vocab-dcat-3/#Class:Dataset_Series).
- DCATDistribution - a subclass of DCATResource, corresponds [DCAT Distribution](https://www.w3.org/TR/vocab-dcat-3/#Class:Distribution).
- DataService - a subclass of DCATResource, corresponds [DCAT Data Service](https://www.w3.org/TR/vocab-dcat-3/#Class:Data_Service).

Along with a number of supporting classes:

- DCAT profile classes
  - PeriodOfTime - [DCAT Period of Time](https://www.w3.org/TR/vocab-dcat-3/#Class:Period_of_Time) class
  - Location - [DCTERMS Location](https://www.w3.org/TR/vocab-dcat-3/#Class:Location)
  - Checksum - [SPDX Checksum](https://www.w3.org/TR/vocab-dcat-3/#Class:Checksum)
- OWL Time ontology classes
  - GeneralDateTimeDescription - [OWL General Date Time Description](https://www.w3.org/TR/owl-time/#time:GeneralDateTimeDescription)
  - DateTimeDescription - [OWL Date Time Description](https://www.w3.org/TR/owl-time/#time:DateTimeDescription)
  - TimeInstant - [OWL Time Instant](https://www.w3.org/TR/owl-time/#time:Instant)
  - TimePosition - [OWL Time Position](https://www.w3.org/TR/owl-time/#time:TimePosition)
- PROV Ontology classes
  - Activity - [PROV-O Activity](https://www.w3.org/TR/prov-o/#Activity)
  - Association - [PROV-O Association](https://www.w3.org/TR/prov-o/#Association)
  - End - [PROV-O End](https://www.w3.org/TR/prov-o/#End)
  - EntityInfluence - [PROV-O EntityInfluence](https://www.w3.org/TR/prov-o/#EntityInfluence)
  - InstantaneousEvent - [PROV-O InstantaneousEvent](https://www.w3.org/TR/prov-o/#InstantaneousEvent)
  - Start - [PROV-O Start](https://www.w3.org/TR/prov-o/#Start)
- Policy [ODLR Policy](https://www.w3.org/TR/odrl-vocab/#policyConcepts)
- vCard [Minimal implementation of vCard](https://www.w3.org/TR/vcard-rdf/)
- Agent [Health-RI interpretation of PROV Agent](https://health-ri.atlassian.net/wiki/spaces/FSD/pages/121110529/Core+Metadata+Schema+Specification#Agent)

Package includes **Health-RI core model** following classes

- Project [FOAF Project implementation](http://xmlns.com/foaf/spec/#term_Project)
- HRIDataset
- HRICatalog
- HRIDistribution
- HRIDataService

Note: Health-RI core model is a more strict one cardinality-wise and regarding mandatory and recommended fields than
DCAT-AP profile. There's no child-parent relationship implemented for HRI models.

### Namespaces

The package reuses common namespaces defined in `rdflib`. Additionally following namespaces are defined and available
from the package:

- DCATv3 - extension for DCAT rdflib namespace to include attributes added in v3
- ADMS (the Asset Description Metadata Schema), generated based on [Official specification](https://uri.semic.eu/w3c/ns/adms.ttl)
- FREQ - the Collection Description Frequency Namespace, generated based on [Dublin core frequency specification](https://www.dublincore.org/specifications/dublin-core/collection-description/frequency/freq.rdf)
- GEOSPARQL - GeoSPARQL Ontology Namespace, generated based on [Open Geospatial Consortium documentation](https://opengeospatial.github.io/ogc-geosparql/geosparql11/geo.ttl#)
- LOCN - ISA Location Core Vocabulary Namespace, generated based on [ISA Programme Location Core Vocabulary specification](https://semiceu.github.io/Core-Location-Vocabulary/releases/w3c/locn.ttl)

### Enum classes

In case RDF property range is defined by an ontology following `enum` classes are used to define choices:

- Status
- AccessRights
- Frequency
- DayOfWeek
- MonthOfYear

## How a model is defined

All the model classes are inherited from RDFModel which is, in its turn, a subclass of pydantic.BaseModel.
RDFModel class provides logic to convert a class instance to an RDF graph.
Information about the class and instructions how a class instance can be converted to RDF graph is defined by
configurations provided in `model_config` and `extra` attributes fields information.

A base model config allows arbitrary type and use of enum values. `json_schema_extra` contains four additional
properties to include in schema:

- `$ontology` - a link to ontology (or a list of links)
- `$namespace` - string namespace link
- `$IRI` - class link within namespace
- `$prefix` - selected prefix, please note the package uses `bind_namespaces="rdflib"` serialization mode,
so most common namespaces are bound with prefixes defined in rdflib. Otherwise, model_config prefix is used.

For example `model_config` for DCATDataset can be:

```python
from pydantic import ConfigDict
from rdflib.namespace import DCAT
from dcat.rdf_model import RDFModel


class DCATDataset(RDFModel):
    model_config = ConfigDict(
        extra="forbid",
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "https://www.w3.org/TR/vocab-dcat-3/",
            "$namespace": str(DCAT),
            "$IRI": DCAT.Resource,
            "$prefix": "dcat"
          }
                                  )
```

Note, strictly speaking all parameters in the example above except `json_schema_extra` are redundant because they are
defined at RDFModel level, we repeat them for explicitness.

Basic information about `Fields` in pydantic models can be found in [official documentation](#https://docs.pydantic.dev/latest/concepts/fields/).
In current package following field info parameters are used to define an attribute:

- `default` - set to None for optional field and missing for mandatory ones
- `description` - to provide info about an attribute
- `extra` - to provide RDF properties for an attribute (see below)
- some other e.g. `pattern` when it is reasonable to validate a field value with regular expression etc.

Two parameters are added as field `extra` information for each field: `rdf_term` - defining RDF term for an attribute,
it defines node's predicate at conversion to RDF graph and `rdf_type`, defining RDF kind of object for a field (see below).

#### RDF types and pydantic field types

In RDF core consept three kinds of objects are defined and can appear in a RDFLib’s graph’s triples: IRIs, Blank Node and Literal.
Despite pydantic supports arbitrary types, RDF Literal or URIRef can not be serialized in JSON schema.
Therefore, any type of standard library types and some pydantic-specific types (e.g. pydantic.AnyUrl, pydantic.AnyHttpUrl)
can be used instead and converted to URIRef or Literal afterward. Possible values for `rdf_type` parameter are
`literal`, `uri`, `rdfs_literal` and `datetime_literal`. In case field value can be a complex object, `rdf_type` should be
set to `uri` so a field definition is as in the following example:

```python
from typing import Union, List
from pydantic import AnyHttpUrl, Field
from dcat.rdf_model import RDFModel
from dcat.dcat_dataset import Frequency
from rdflib.namespace import DCTERMS
from dcat.spatial import Location


class DCATDataset(RDFModel):
  
    frequency: Union[AnyHttpUrl, Frequency] = Field(
        default=None,
        description="The frequency at which a dataset is published.",
        rfd_term=DCTERMS.accrualPeriodicity,
        rdf_type="uri"
    )
    spatial: List[Union[AnyHttpUrl, Location]] = Field(
        default=None,
        description="The geographical area covered by the dataset.",
        alias="geographical_coverage",
        rdf_term=DCTERMS.spatial,
        rdf_type="uri")
```

In the example above `frequency` can be provided as external or internal URL or a value defined by `enum` class
Frequency (which is also a URL). `spatial` may be a Location object or an external or internal link to a location.

### LiteralField

LiteralField class is a subclass of RDFModel to handle RDF Literal type in pydantic model.
For general information regarding RDF terms please review  [RDFLib implementation of RDF types](https://rdflib.readthedocs.io/en/stable/rdf_terms.html)
and [RDF Literal definition](http://www.w3.org/TR/rdf-concepts/#section-Graph-Literal).

The class has the following attributes:

- `datatype` (optional, string, pydantic.AnyUrl) - datatype for literal value, e.g. 'xsd:date'
see <https://www.w3.org/TR/xmlschema-2/#built-in-datatypes>. As per RDF literal specification a link to a datatype is
expected, but it is possible to pass a string as well. If the string starts with "xsd:", the code will try to resolve it with a value within rdflib.XSD namespace.
- `language` (optional, string) - [RFC 3066 language tag](https://datatracker.ietf.org/doc/html/rfc3066.html),
                                a tag listed in [IANA-administrated namespace of language tags](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry) is recommended.
- `value` (string) - literal value associated with literal

`datatype` and `language` are mutually exclusive parameters.

Below there is an example of different ways to instantiate a `LiteralField` object and their usage as DCATDataset data:

```python
from dcat.rdf_model import LiteralField
from dcat.dcat_dataset import DCATDataset
from rdflib import XSD, URIRef

dataset_title = LiteralField(value="Test dataset title", language="en")
dataset_title_nl = LiteralField(value="Titel van de testdataset", language="nl")
description = LiteralField(value="This is description of Test dataset", language="en")
version = LiteralField(value="1.0", datatype="xsd:string")
identifier = LiteralField(value="ts1234", datatype=XSD.string)

dataset = DCATDataset(title=[dataset_title, dataset_title_nl],
                      description=[description],
                      version=[version],
                      identifier=[identifier]
                      )
print(dataset.to_graph(URIRef("http://example.com/ts1234")).serialize())
```

The code above prints out:

```turtle
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://example.com/test_dataset> a dcat:Dataset ;
    dcterms:description "This is description of Test dataset"@en ;
    dcterms:identifier "ts1234"^^xsd:string ;
    dcterms:title "Test dataset title"@en,
        "Titel van de testdataset"@nl ;
    dcat:version "1.0"^^xsd:string .

```

Some attributes such as `title` or `description` expect a LiteralField to be passed as a value. However, we understand
it is not always the case that language or datatype information are available from a source. For better user experience
most such fields accept strings and convert strings to a LiterField with `None` as datatype and language seamlessly as
part of model validation.

## RDF conversion

## JSON/YAML

- either json schema limitation

## Defining a model of your own and extending models

There are two aspects to pay attention:

## Usage examples

[IPython Notebook usage example for time models](Usage_example_time_models.ipynb)
