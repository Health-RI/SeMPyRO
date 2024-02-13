import json
from typing import List, Union
from pathlib import Path
from pydantic import Field, AnyHttpUrl, ConfigDict
from rdflib.namespace import DCAT, FOAF
from dcat.dcat_dataset import DCATDataset


class DCATCatalog(DCATDataset):
    """A curated collection of metadata about resources."""
    model_config = ConfigDict(title=DCAT.Catalog)

    catalog_record: AnyHttpUrl = Field(
        default=None,
        description="A record describing the registration of a single resource (e.g., a dataset, a data service) that "
                    "is part of the catalog.",
        rdf_term=DCAT.record,
        rdf_type="uri"
    )
    dataset: List[AnyHttpUrl] = Field(
        default=None,
        description="A dataset that is listed in the catalog.",
        rdf_term=DCAT.dataset,
        rdf_type="uri"
    )
    service: List[AnyHttpUrl] = Field(
        default=None,
        description="A service that is listed in the catalog.",
        rdf_term=DCAT.service,
        rdf_type="uri"
    )
    catalog: List[AnyHttpUrl] = Field(
        default=None,
        description="A catalog that is listed in the catalog.",
        rdf_term=DCAT.catalog,
        rdf_type="uri"
    )
    homepage: AnyHttpUrl = Field(
        default=None,
        description="A homepage of the catalog (a public Web document usually available in HTML).",
        rdf_term=FOAF.homepage,
        rdf_type="uri"
    )
    themes: List[AnyHttpUrl] = Field(
        default=None,
        description="A knowledge organization system (KOS) used to classify the resources documented in the catalog "
                    "(e.g., datasets and services).",
        rdf_term=DCAT.themeTaxonomy,
        rdf_type="uri"
    )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parent.resolve(), "json_models")
    with open(Path(json_models_folder, "DCATCatalog.json"), "w") as schema_file:
        model_schema = DCATCatalog.model_json_schema()
        json.dump(model_schema, schema_file, indent=2)
