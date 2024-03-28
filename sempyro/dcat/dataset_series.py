from pathlib import Path

from sempyro.dcat.dcat_dataset import DCATDataset
from pydantic import ConfigDict
from rdflib import DCAT

from sempyro.namespaces import DCATv3


class DatasetSeries(DCATDataset):
    """A collection of datasets that are published separately, but share some characteristics that group them"""
    model_config = ConfigDict(title=DCATv3.DatasetSeries,
                              json_schema_extra={
                                  "$ontology": "https://www.w3.org/TR/vocab-dcat-3/",
                                  "$namespace": str(DCAT),
                                  "$IRI": DCATv3.DatasetSeries,
                                  "$prefix": "dcat"
                              }
                              )


if __name__ == "__main__":
    json_models_folder = Path(Path(__file__).parents[2].resolve(), "models", "dcat")
    DatasetSeries.save_schema_to_file(Path(json_models_folder, "DatasetSeries.json"), "json")
    DatasetSeries.save_schema_to_file(Path(json_models_folder, "DatasetSeries.yaml"), "yaml")
