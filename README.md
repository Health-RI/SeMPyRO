# HRIPydanticModels

**SeMPyRO** is a Python package containing Pydantic models representing classes of the
DCAT-AP v3 data model. It is designed to streamline data validation, conversion to RDF, and schema generation processes.

## Key Features

- **Data Validation**: Easily validate data against schemas, ensuring its correctness, integrity and DCAT-AP compatibility.
- **RDF Graph Conversion**: Convert data into RDF graphs effortlessly, enabling integration with RDF-based systems and applications.
- **Schema Generation**: Generate JSON/YAML schemas compatible with the DCAT-AP v3 profile, facilitating interoperability and compliance with standards.
- **Pedantic Integration**: Built upon the robust [Pydantic](https://docs.pydantic.dev/) library, leveraging its powerful validation capabilities and extending them for RDF handling.

## Background

### DCAT

DCAT is an RDF vocabulary designed to facilitate interoperability between data catalogs published on the Web.

DCAT enables a publisher to describe datasets and data services in a catalog using a standard model and vocabulary
that facilitates the consumption and aggregation of metadata from multiple catalogs. This can increase the
discoverability of datasets and data services. It also makes it possible to have a decentralized approach to publishing
data catalogs and makes federated search for datasets across catalogs in multiple sites possible using the same query
mechanism and structure. Aggregated DCAT metadata can serve as a manifest file as part of the digital preservation
process.

[Official DCAT v3 specification](https://www.w3.org/TR/vocab-dcat-3/)

### DCAT-AP

DCAT-AP is a DCAT profile for sharing information about Catalogues containing Datasets and Data Services descriptions
in Europe, under maintenance by the SEMIC action, Interoperable Europe. This Application Profile provides a minimal
common basis within Europe to share Datasets and Data Services cross-border and cross-domain.

[Official DCAT-AP v3 specification](https://semiceu.github.io/DCAT-AP/releases/3.0.0/)

### Health-RI core data model

Health-RI is a no profit organization in the Netherlands dedicated to improving the reuse of health data for policy, 
research, and innovation to achieve a learning healthcare system.
We have published a [Core Metadata Model](https://health-ri.atlassian.net/l/cp/udWLxwpu) based on DCAT-AP 
specification for the sharing of Dutch healthcare-related datasets.
Current package includes Pydantic classes for the **Health-RI Core model**.

## Installation

To install the package run
```commandline
pip install sempyro
```

[Documentation](./docs) folder contains usage examples executable in Jupiter Notebook. 
If you want to explore them follow [official Jupyter installation guid](https://jupyter.org/install#jupyter-notebook).
Additionally you may need to install pandas and/or [erdantic](./docs/Defining_extendind_a_model.md#visualization-with-erdantic).

## Licence

[Apache-2.0](./LICENSE)

## Documentation

For more information on package content and usage please review [documentation](./docs).
