from typing import List, Dict, Any

from data import Source
import domain.model_api as mapi


def create_sources(*sources: Dict[str, Any]) -> List[Source]:
    """
    Create sources into the database
    """
    return mapi.create_objects(Source, *sources)


def delete_sources(*sources: Source):
    """
    Delete sources from the database
    """
    return mapi.delete_objects(*sources)


def create_source(**kwargs) -> Source:
    """
    Create a given source into the database according to the parameters
    """
    return mapi.create_object(Source, **kwargs)


def update_source(source: Source, **kwargs) -> Source:
    """
    Update the source into the database according to the parameters
    """
    return mapi.update_object(source, **kwargs)


def delete_source(source: Source) -> Source:
    """
    Delete the source from the database
    """
    return mapi.delete_object(source)
