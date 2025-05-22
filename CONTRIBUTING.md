# Contributing to SeMPyRO

Thank you for your interest in contributing to SeMPyRO! Your participation helps make this project better for everyone.

All types of contributions are valued and appreciated, whether it's reporting bugs, suggesting features, improving documentation, or adding code.

## Questions and Bug Reports

If you have a question or encounter a bug, please file an Issue on our repository. When reporting bugs, include:

- Clear steps to reproduce the issue
- Relevant environment details (operating system, Python version)
- SeMPyRO version you're using
- Expected behavior versus actual behavior
- Any error messages or logs

## Guidelines for Adding Models

See [Defining a model of your own and extending models](./docs/Defining_extending_a_model.md) for a tutorial on
how to add and extend models. 
When contributing new models to SeMPyRO, please follow these practices:

### Inheritance and Properties

- When subclassing existing models, reuse properties whenever possible
- Only override properties when there's a meaningful technical difference (e.g., different cardinality or type)
- Maintain consistent behavior patterns across related models

Properties with a range that can refer to externally defined classes, e.g., the property `distribution` of a `DCATDataset`
that has a range of `DCATDistribution`, should have the type `Union[AnyHttpUrl, DCATDistribution]`. This approach allows
the `DCATDataset` class to be used by directly assigning the `DCATDistribution` class or by supplying the URI 
for the Distribution class.

If a property has the range rdfs:Literal, and it may include a language tag (e.g., "text"@en), then its type should be 
defined as LiteralField. However, to accommodate users who might provide a plain string without specifying a language 
tag, the property should accept both types. Therefore, use the union type Union[str, LiteralField].

Properties with the range `rdfs:Literal` should have `rdf_type` in `json_schema_extra` equal to `rdfs_literal`, 
`datetime_literal` or an `xsd` type. If the range is a URI, `rdf_type` should be `uri`.

### Naming Conventions

- Property names should match those in the application profile, not necessarily the RDF term
- Example: For a Dataset in DCAT-AP v3, use `release_date` instead of `issued` (from `dct:issued`)
- Replace spaces in property names with underscores (e.g., `access_rights` not `access rights`)

### Namespaces and Vocabularies

- If your model requires a namespace not already defined for the `rdf_term` in `json_schema_extra`, add it to `sempyro/namespaces`
- Follow the existing namespace declaration patterns for consistency
- Define vocabularies in a `vocabularies.py` file within your model's directory
- Ensure vocabulary terms are properly documented and follow established patterns

### Code Quality

- Include appropriate tests for your model
- Add documentation that explains the purpose and usage of your model
- Follow the project's coding style and conventions