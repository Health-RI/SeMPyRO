import json
from pathlib import Path
from pydantic import ConfigDict, AnyHttpUrl, Field
from rdflib.namespace import DCAT
from typing import List, Union

from dcat_resource import DCATResource
from dcat_dataset import DCATDataset


class DatasetSeries(DCATResource):
    """A collection of operations that provides access to one or more datasets or data processing functions."""
    model_config = ConfigDict(title=DCAT.DataService)

    endpoint_description: List[Union[AnyHttpUrl, DCATResource]] = Field(
        default=None,
        description="A description of the services available via the end-points, including their operations, "
                    "parameters etc.",
        rdf_term=DCAT.endpointDescription,
        rdf_type="uri"
    )
    endpoint_url: List[Union[AnyHttpUrl, DCATResource]] = Field(
        description="The root location or primary endpoint of the service (a Web-resolvable IRI).",
        rdf_term=DCAT.endpointURL,
        rdf_type="uri"
    )
    serves_dataset: List[Union[AnyHttpUrl, DCATDataset]] = Field(
        default=None,
        description="A collection of data that this data service can distribute.",
        rdf_term=DCAT.servesDataset,
        rdf_type="uri"
    )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parent.resolve(), "json_models")
    with open(Path(json_models_folder, "DatasetSeries.json"), "w") as schema_file:
        model_schema = DatasetSeries.model_json_schema()
        json.dump(model_schema, schema_file, indent=2)
