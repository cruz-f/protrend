from typing import List

from data import Source
import domain.model_api as mapi


def get_sources() -> List[Source]:
    """
    Get sources list from database
    """
    return mapi.get_objects(Source)


def filter_sources(*args, **kwargs) -> List[Source]:
    """
    Get and filter sources from database
    """
    return mapi.filter_objects(Source, *args, **kwargs)


def order_by_sources(*fields) -> List[Source]:
    """
    Get and order by sources from database
    """
    return mapi.order_by_objects(Source, *fields)


def order_sources_by_id() -> List[Source]:
    """
    Get and order by sources by protrend identifier from database
    """
    return mapi.order_by_objects(Source, 'protrend_id')


def get_source(**kwargs) -> Source:
    """
    Get a given source from database
    """
    return mapi.get_object(Source, **kwargs)


def get_source_by_id(protrend_id: str) -> Source:
    """
    Get a given source from database using the protrend identifier
    """
    return mapi.get_object(Source, protrend_id=protrend_id)


def get_last_source() -> Source:
    """
    Get the last source from database using the protrend identifier
    """
    return mapi.get_last_object(Source, 'protrend_id')
