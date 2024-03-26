from importlib.metadata import version

__version__ = version("sempyro")

__all__ = (
    "dcat",
    "hri_dcat",
    "namespaces",
    "utils"
    )


def __dir__() -> 'list[str]':
    return list(__all__)
