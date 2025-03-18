# Models and other objects

**Table of contents:**

- [Types of objects the package includes](#types-of-objects-the-package-includes)
  - [Model classes](#model-classes)
  - [Namespaces](#namespaces)
  - [Enum classes](#enum-classes)
- [How a model is defined](#how-a-model-is-defined)
- [Explore Model annotation](#explore-model-annotation)
- [Data validation](#data-validation)
- [Defining a model of your own and extending models](#defining-a-model-of-your-own-and-extending-models)
- [Usage examples](#usage-examples)

## Types of objects the package includes

The package comprises three types of classes to implement the DCAT model and its derivatives: 
- Pydantic-based model classes, 
- RDF namespaces and
- `enum` classes, representing vocabularies.

### Model classes

All the model classes are inherited from `RDFModel` which is, in its turn, a subclass of `pydantic.BaseModel`.

#### DCAT-AP v3
The following classes that implement the DCAT-AP v3 model are available in the package:

- DCATResource is an abstract class corresponding [DCAT Resource](https://www.w3.org/TR/vocab-dcat-3/#Class:Resource) definition.
- DCATDataset - a subclass of DCATResource, corresponds [DCAT Dataset](https://www.w3.org/TR/vocab-dcat-3/#Class:Dataset).
- DCATCatalog - a subclass of DCATDataset, corresponds [DCAT Catalog](https://www.w3.org/TR/vocab-dcat-3/#Class:Catalog_Record).
- DCATDatasetSeries - a subclass of DCATDataset, corresponds [DCAT Dataset Series](https://www.w3.org/TR/vocab-dcat-3/#Class:Dataset_Series).
- DCATDistribution - a subclass of DCATResource, corresponds [DCAT Distribution](https://www.w3.org/TR/vocab-dcat-3/#Class:Distribution).
- DCATDataService - a subclass of DCATResource, corresponds [DCAT Data Service](https://www.w3.org/TR/vocab-dcat-3/#Class:Data_Service).

```python
# to import 
from sempyro.dcat import DCATResource, DCATDataset, DCATCatalog, DCATDistribution, DCATDatasetSeries, DCATDataService
```

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

```python
# to import
from sempyro.time import PeriodOfTime, TimeInstant, TimePosition, GeneralDateTimeDescription, DateTimeDescription
from sempyro.geo import Location, Geometry
from sempyro.prov import Activity, Association, End, EntityInfluence, InstantaneousEvent
from sempyro.odrl import ODRLPolicy
from sempyro.vcard import VCard
from sempyro.foaf import Agent
```

#### Health-RI core metadata model

This package includes the following classes for the **Health-RI core model**:

- Project, an [FOAF Project implementation](http://xmlns.com/foaf/spec/#term_Project)
- HRIDataset
- HRICatalog
- HRIDistribution
- HRIDataService
```python
# to import
from sempyro.hri_dcat import HRIDataset, HRICatalog, HRIDistribution, HRIDataService
```

Note: The Health-RI core model imposes more restrictions on the cardinality, e.g., regarding mandatory and recommended
properties, than the DCAT-AP v3 model. Classes implementing the Health-RI model are an extension of the DCAT models.

### Namespaces

The package reuses common namespaces defined in `rdflib`. Additionally the following namespaces are defined and available
from the package:

- DCATv3 - extension for DCAT rdflib namespace to include attributes added in v3
- ADMS (the Asset Description Metadata Schema), generated based on [Official specification](https://uri.semic.eu/w3c/ns/adms.ttl)
- FREQ - the Collection Description Frequency Namespace, generated based on [Dublin core frequency specification](https://www.dublincore.org/specifications/dublin-core/collection-description/frequency/freq.rdf)
- GEOSPARQL - GeoSPARQL Ontology Namespace, generated based on [Open Geospatial Consortium documentation](https://opengeospatial.github.io/ogc-geosparql/geosparql11/geo.ttl#)
- LOCN - ISA Location Core Vocabulary Namespace, generated based on [ISA Programme Location Core Vocabulary specification](https://semiceu.github.io/Core-Location-Vocabulary/releases/w3c/locn.ttl)
- Greg - [OWL-Time Gregorian Calendar](https://www.w3.org/ns/time/gregorian#) namespace
```python
# to import
from sempyro.namespaces import DCATv3, ADMS, FREQ, GeoSPARQL, LOCN, Greg
```

### Enum classes

In case RDF property range is defined by an ontology following `enum` classes are used to define choices:

- Status, based on ADMSStatus
- AccessRights, based on the [European Access Right vocabulary](https://publications.europa.eu/resource/authority/access-right)
- Frequency
- DayOfWeek
- MonthOfYear
- DatasetTheme, based on the [European Data Theme vocabulary](http://publications.europa.eu/resource/authority/data-theme)
- GeonovumLicenses, based on the [Geonovum License vocabulary](https://definities.geostandaarden.nl/dcat-ap-nl/id/waardelijst/licenties)

```python
from sempyro.dcat import Status, AccessRights, Frequency
from sempyro.time import DayOfWeek, MonthOfYear
from sempyro.hri_dcat import DatasetTheme, GeonovumLicences
```

## How a model is defined

All the model classes are inherited from RDFModel which is, in its turn, a subclass of pydantic.BaseModel.
RDFModel class provides logic to convert a class instance to an RDF graph.
Information about the class and instructions how a class instance can be converted to RDF graph is defined by
configurations provided in `model_config` and `extra` attributes fields information.

A base model config allows arbitrary type and use of enum values, forces assignment validations.
`json_schema_extra` contains four additional properties to include in schema:

- `$ontology` - a link to ontology (or a list of links)
- `$namespace` - string namespace link
- `$IRI` - class link within namespace
- `$prefix` - selected prefix, please note the package uses `bind_namespaces="rdflib"` serialization mode,
so most common namespaces are bound with prefixes defined in rdflib. Otherwise, model_config prefix is used.

For example `model_config` for DCATDataset can be:

```python
from pydantic import ConfigDict
from rdflib.namespace import DCAT
from sempyro import RDFModel


class DCATDataset(RDFModel):
  model_config = ConfigDict(
    extra="forbid",
    arbitrary_types_allowed=True,
    use_enum_values=True,
    validate_assignment=True,
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
In rare cases `extra` field configuration can be extended with `bind_namespace` with a tuple of prefix and string namespace.
It can be used if field property is from another namespace than the model itself and the namespace is not one of the RDF standard namespaces.

### RDF types and pydantic field types

In RDF core consept three kinds of objects are defined and can appear in a RDFLib’s graph’s triples: IRIs, Blank Node and Literal.
Despite pydantic supports arbitrary types, RDF Literal or URIRef can not be serialized in JSON schema.
Therefore, any type of standard library types and some pydantic-specific types (e.g. pydantic.AnyUrl, pydantic.AnyHttpUrl)
can be used instead and converted to URIRef or Literal afterward. Possible values for `rdf_type` parameter are
`literal`, `uri`, `rdfs_literal` and `datetime_literal`. In case field value can be a complex object, `rdf_type` should be
set to `uri` so a field definition is as in the following example:

```python
from typing import Union, List
from pydantic import AnyHttpUrl, Field
from sempyro import RDFModel
from sempyro.dcat import Frequency
from rdflib.namespace import DCTERMS
from sempyro.geo import Location


class DCATDataset(RDFModel):
  frequency: Union[AnyHttpUrl, Frequency] = Field(
    default=None,
    description="The frequency at which a dataset is published.",
    json_schema_extra={
      "rdf_term": DCTERMS.accrualPeriodicity,
      "rdf_type": "uri"
    }
  )
  spatial: List[Union[AnyHttpUrl, Location]] = Field(
    default=None,
    description="The geographical area covered by the dataset.",
    alias="geographical_coverage",
    json_schema_extra={
      "rdf_term": DCTERMS.spatial,
      "rdf_type": "uri"
    }
  ) 
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
from sempyro import LiteralField
from sempyro.dcat import DCATDataset
from rdflib import XSD, URIRef

dataset_title = LiteralField(value="Test dataset title", language="en")
dataset_title_nl = LiteralField(value="Titel van de test dataset", language="nl")
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

## Explore Model annotation

**SemPyRO** uses pydantic `FieldInfo` in a way that a class can be a documentation of itself.
To get a quick and easy access to model field definitions one can use pydantic `BaseModel.model_fields` and/or 
a number of methods implemented for model annotation

#### Pydantic `BaseModel.model_fields`

```python
from sempyro.dcat import DCATDataset
import pprint

pprint.pprint(DCATDataset.model_fields)
```
outputs in list of fields with annotations in alphabetical order:
```text
{'access_rights': FieldInfo(annotation=AccessRights, required=False, description='Information about who can access the resource or an indication of its security status.', json_schema_extra={'rdf_term': rdflib.term.URIRef('http://purl.org/dc/terms/accessRights'), 'rdf_type': 'uri'}),
 'conforms_to': FieldInfo(annotation=Url, required=False, description='An established standard to which the described resource conforms.', json_schema_extra={'rdf_term': rdflib.term.URIRef('http://purl.org/dc/terms/conformsTo'), 'rdf_type': 'uri'}, metadata=[UrlConstraints(max_length=None, allowed_schemes=['http', 'https'], host_required=None, default_host=None, default_port=None, default_path=None)]),
 'contact_point': FieldInfo(annotation=List[Union[Annotated[Url, UrlConstraints(max_length=None, allowed_schemes=['http', 'https'], host_required=None, default_host=None, default_port=None, default_path=None)], VCard, Agent]], required=False, description='Relevant contact information for the cataloged resource. Use of vCard is recommended', json_schema_extra={'rdf_term': rdflib.term.URIRef('http://www.w3.org/ns/dcat#contactPoint'), 'rdf_type': 'uri'}),
 'creator': FieldInfo(annotation=List[Union[Annotated[Url, UrlConstraints(max_length=None, allowed_schemes=['http', 'https'], host_required=None, default_host=None, default_port=None, default_path=None)], VCard, Agent]], required=False, description='The entity responsible for producing the resource. Resources of type foaf:Agent are recommended as values for this property.', json_schema_extra={'rdf_term': rdflib.term.URIRef('http://purl.org/dc/terms/creator'), 'rdf_type': 'uri'}),
 'description': FieldInfo(annotation=List[LiteralField], required=True, description='A free-text account of the resource.', json_schema_extra={'rdf_term': rdflib.term.URIRef('http://purl.org/dc/terms/description'), 'rdf_type': 'literal'}),
 'distribution': FieldInfo(annotation=List[Annotated[Url, UrlConstraints(max_length=None, allowed_schemes=['http', 'https'], host_required=None, default_host=None, default_port=None, default_path=None)]], required=False, description='An available distribution of the dataset.', json_schema_extra={'rdf_term': rdflib.term.URIRef('http://www.w3.org/ns/dcat#distribution'), 'rdf_type': 'uri'}),
<...> }
```
#### RDFModel field annotations
- Get mandatory fields
```python
from sempyro.dcat import DCATDataset
import pprint

model_fields = DCATDataset.annotate_model()
pprint.pprint(model_fields.mandatory_fields())
```
```text
['description', 'title']
```
- Get fields description
```python
pprint.pprint(model_fields.fields_description())
```
```text
{'access_rights': 'Information about who can access the resource or an '
                  'indication of its security status.',
 'conforms_to': 'An established standard to which the described resource '
                'conforms.',
 'contact_point': 'Relevant contact information for the cataloged resource. '
                  'Use of vCard is recommended',
 'creator': 'The entity responsible for producing the resource. Resources of '
            'type foaf:Agent are recommended as values for this property.',
 'description': 'A free-text account of the resource.',
 'distribution': 'An available distribution of the dataset.',
 <...> }
```
- Get fields type
```python
pprint.pprint(model_fields.get_fields_types())
```
```text
{'access_rights': {'Datatype': 'AccessRights', 'RDF type': 'uri'},
 'conforms_to': {'Datatype': 'Url', 'RDF type': 'uri'},
 'contact_point': {'Datatype': 'List[Union[Url, VCard, Agent]]',
                   'RDF type': 'uri'},
 'creator': {'Datatype': 'List[Union[Url, VCard, Agent]]', 'RDF type': 'uri'},
 'description': {'Datatype': 'List[LiteralField]', 'RDF type': 'literal'},
 <...> }
```
Note, `List` type is provided for fields with cardinality greater than 1.

- How fields relate to RDF properties
```python
pprint.pprint(model_fields.get_rdf_correspondence())
```
```text
{'access_rights': rdflib.term.URIRef('http://purl.org/dc/terms/accessRights'),
 'conforms_to': rdflib.term.URIRef('http://purl.org/dc/terms/conformsTo'),
 'contact_point': rdflib.term.URIRef('http://www.w3.org/ns/dcat#contactPoint'),
 'creator': rdflib.term.URIRef('http://purl.org/dc/terms/creator'),
 'description': rdflib.term.URIRef('http://purl.org/dc/terms/description'),
 <...> }
```
- Get default values if available, e.g.
```python
from sempyro.time import DateTimeDescription

model_fields = DateTimeDescription.annotate_model()
pprint.pprint(model_fields.fields_defaults())
```
```text
{'hasTRS': 'http://www.opengis.net/def/uom/ISO-8601/0/Gregorian'}
```
## RDF conversion

An instance of a model of `RDFModel` type class can be converted to an RDF graph by calling `RDFModel.to_graph(subject)`.
It is also possible to add an `RDFModel` type model instance as a node of preexisting graph with `to_graph_node` function 
and providing following arguments: 
- `graph` - the RDF graph to add a node to;
- `subject` -subject to link the node to;
- `node_predicate` - a URIRef predicate for the node
- `node_type` - a URIRef describing range of the node. 

Let's consider creating a dataset whose spatial coverage corresponds to Anne Frank's house in Amsterdam, specified as a 
polygon (the coordinate reference system is CRS84). It can be done in three ways:

1. With DCATDataset class:
```python
from sempyro import LiteralField
from sempyro.dcat import DCATDataset
from sempyro.geo import Location
from sempyro.namespaces import GeoSPARQL
from rdflib import URIRef

# Initiate Location instance
polygon_string = """POLYGON ((
      4.8842353 52.375108 , 4.884276 52.375153 ,
      4.8842567 52.375159 , 4.883981 52.375254 ,
      4.8838502 52.375109 , 4.883819 52.375075 ,
      4.8841037 52.374979 , 4.884143 52.374965 ,
      4.8842069 52.375035 , 4.884263 52.375016 ,
      4.8843200 52.374996 , 4.884255 52.374926 ,
      4.8843289 52.374901 , 4.884451 52.375034 ,
      4.8842353 52.375108
    ))"""
geometry = LiteralField(value=polygon_string, datatype=GeoSPARQL.wktLiteral)
location = Location(geometry=geometry)

dataset = DCATDataset(
  title=["Anne Frank house"],
  description=["Spatial coverage of Anne Frank's house in Amsterdam"],
  spatial=[location]
)

dataset.to_graph(URIRef("http://example.com#Anne_Frank_0")).serialize()
```
which outputs in the following:
```text
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix ns1: <http://www.w3.org/ns/locn#> .

<http://example.com#Anne_Frank_0> a dcat:Dataset ;
    dcterms:description "Spatial coverage of Anne Frank's house in Amsterdam" ;
    dcterms:spatial [ a dcterms:Location ;
            locn:geometry """POLYGON ((
      4.8842353 52.375108 , 4.884276 52.375153 ,
      4.8842567 52.375159 , 4.883981 52.375254 ,
      4.8838502 52.375109 , 4.883819 52.375075 ,
      4.8841037 52.374979 , 4.884143 52.374965 ,
      4.8842069 52.375035 , 4.884263 52.375016 ,
      4.8843200 52.374996 , 4.884255 52.374926 ,
      4.8843289 52.374901 , 4.884451 52.375034 ,
      4.8842353 52.375108
    ))"""^^geo:wktLiteral ] ;
    dcterms:title "Anne Frank house" .
```
2. The same can be achieved by adding Location object to a pre-created graph:
```python
from sempyro import LiteralField
from sempyro.geo import Location
from sempyro.namespaces import GeoSPARQL, LOCN
from rdflib import URIRef, DCAT, DCTERMS, Graph, RDF

graph = Graph()
subject = URIRef("http://example.com#AnneFrank_0")
actual_graph.add((subject, RDF.type, DCAT.Dataset))
actual_graph.bind("locn", LOCN)

polygon_string = """POLYGON ((
  4.8842353 52.375108 , 4.884276 52.375153 ,
  4.8842567 52.375159 , 4.883981 52.375254 ,
  4.8838502 52.375109 , 4.883819 52.375075 ,
  4.8841037 52.374979 , 4.884143 52.374965 ,
  4.8842069 52.375035 , 4.884263 52.375016 ,
  4.8843200 52.374996 , 4.884255 52.374926 ,
  4.8843289 52.374901 , 4.884451 52.375034 ,
  4.8842353 52.375108
))"""
geometry = LiteralField(value=polygon_string, datatype=GeoSPARQL.wktLiteral)
location = Location(geometry=geometry)

location.to_graph_node(graph=graph,
                       subject=subject,
                       node_predicate=DCTERMS.spatial,
                       node_type=DCTERMS.Location)

print(graph.serialize())
```
3. It is also possible to create a class instance with mandatory fields only first and add optional ones then:
```python
from sempyro import LiteralField
from sempyro.dcat import DCATDataset
from sempyro.geo import Location
from sempyro.namespaces import GeoSPARQL
from rdflib import URIRef

# Create dataset
dataset = DCATDataset(
  title=["Anne Frank house"],
  description=["Spatial coverage of Anne Frank's house in Amsterdam"]
)
# Initiate Location instance
polygon_string = """POLYGON ((
      4.8842353 52.375108 , 4.884276 52.375153 ,
      4.8842567 52.375159 , 4.883981 52.375254 ,
      4.8838502 52.375109 , 4.883819 52.375075 ,
      4.8841037 52.374979 , 4.884143 52.374965 ,
      4.8842069 52.375035 , 4.884263 52.375016 ,
      4.8843200 52.374996 , 4.884255 52.374926 ,
      4.8843289 52.374901 , 4.884451 52.375034 ,
      4.8842353 52.375108
    ))"""
geometry = LiteralField(value=polygon_string, datatype=GeoSPARQL.wktLiteral)
location = Location(geometry=geometry)
# Add property
dataset.spatial=[location]
print(dataset.to_graph(URIRef("http://example.com#Anne_Frank_0")).serialize())
```

## JSON/YAML

Each model can be serialized to .json or .yaml schema and saved to a file with `save_schema_to_file` function 
taking two arguments:
- path - absolute path to file
- file_format - either "json" or "yaml", "json" is default

**NB!** There is a **known limitation** for pydantic json serialization: "oneOf" is not implemented.

## Data validation

The package performs validation to ensure correct data types are used. 

Models are protected from providing extra fields, for example the following code:

```python
from sempyro.dcat import DCATDataset
from sempyro import LiteralField

my_dataset = DCATDataset(**{
  "title": [LiteralField(**{"value": "My dataset", "language": "en"})],
  "description": [LiteralField(**{"value": "What my dataset is about", "language": "en"})],
  "contact_information": "my_email@email.com"
})
```
throws extra vialation error:
```text
pydantic_core._pydantic_core.ValidationError: 1 validation error for DCATDataset
contact_information
  Extra inputs are not permitted [type=extra_forbidden, input_value='my_email@email.com', input_type=str]
    For further information visit https://errors.pydantic.dev/2.5/v/extra_forbidden
```
Skipping mandatory fields is not allowed:

```python
from sempyro.dcat import DCATDataset
from sempyro import LiteralField

my_dataset = DCATDataset(**{
  "title": [LiteralField(**{"value": "My dataset", "language": "en"})],
})

```
```text
pydantic_core._pydantic_core.ValidationError: 1 validation error for DCATDataset
description
  Field required [type=missing, input_value={'title': ['My dataset']}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.5/v/missing
```
Fields datatypes are also checked. In the example below `contact_point` is expected to be list of objects of type 
VCard, Agents or URL (or a combination of them).
```python
from sempyro.dcat import DCATDataset
from sempyro import LiteralField

my_dataset = DCATDataset(**{
  "title": [LiteralField(**{"value": "My dataset", "language": "en"})],
  "description": [LiteralField(**{"value": "What my dataset is about", "language": "en"})],
  "contact_point": ["my_email@email.com"]
})
```
A string was provided, therefore instead:
```text
contact_point.0.url['http','https']
  Input should be a valid URL, relative URL without a base [type=url_parsing, input_value='my_email@email.com', input_type=str]
    For further information visit https://errors.pydantic.dev/2.5/v/url_parsing
contact_point.0.VCard
  Input should be a valid dictionary or instance of VCard [type=model_type, input_value='my_email@email.com', input_type=str]
    For further information visit https://errors.pydantic.dev/2.5/v/model_type
contact_point.0.Agent
  Input should be a valid dictionary or instance of Agent [type=model_type, input_value='my_email@email.com', input_type=str]
    For further information visit https://errors.pydantic.dev/2.5/v/model_type
```
When creating a ETL script for you data it maybe convenient to validate data even before models are instantiated with the data 
and remove invalid records beforehand. It can be done with pydantic `model_validate_json`, data should be a json string:

```python
from sempyro.dcat import DCATDataset
from sempyro.namespaces import GeoSPARQL
import json

data = {
    "title": [{"value": "My dataset", "language": "en"}],
    "description": [{"value": "What my dataset is about", "language": "en"}],
    "spatial": [{"bounding_box": {"value": "POLYGON((-180 90,180 90,180 -90,-180 -90,-180 90))",
                                  "datatype": GeoSPARQL.wktLiteral}}]
}

DCATDataset.model_validate_json(json.dumps(data))

```
The example above passes the validation successfully. Note how the package recognizes and the structure of nested objects
(LiteralField for title and description and Location for spatial).

## Defining a model of your own and extending models

Please review the [following page](Defining_extending_a_model) to learn more on how to extend a model or
create one of your own.

## Usage examples

[IPython Notebook usage example for time models](Usage_example_time_models.ipynb)

[IPython Notebool usage example for DCATDataset from source data to FDP](Usage_example_with_test_data.ipynb)
