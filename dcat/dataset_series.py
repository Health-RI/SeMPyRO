from pydantic import ConfigDict

from dcat_dataset import DCATDataset
from namespaces.DCATv3 import DCATv3


class DatasetSeries(DCATDataset):
    """A collection of datasets that are published separately, but share some characteristics that group them"""
    model_config = ConfigDict(title=DCATv3.DatasetSeries)
