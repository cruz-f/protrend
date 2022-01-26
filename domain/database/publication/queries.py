from typing import List

from data import Publication
import domain.model_api as mapi


def get_publications() -> List[Publication]:
    """
    Get publications list from database
    """
    return mapi.get_objects(Publication)


def filter_publications(*args, **kwargs) -> List[Publication]:
    """
    Get and filter publications from database
    """
    return mapi.filter_objects(Publication, *args, **kwargs)


def order_by_publications(*fields) -> List[Publication]:
    """
    Get and order by publications from database
    """
    return mapi.order_by_objects(Publication, *fields)


def order_publications_by_id() -> List[Publication]:
    """
    Get and order by publications by protrend identifier from database
    """
    return mapi.order_by_objects(Publication, 'protrend_id')


def get_publication(**kwargs) -> Publication:
    """
    Get a given publication from database
    """
    return mapi.get_object(Publication, **kwargs)


def get_publication_by_id(protrend_id: str) -> Publication:
    """
    Get a given publication from database using the protrend identifier
    """
    return mapi.get_object(Publication, protrend_id=protrend_id)


def get_last_publication() -> Publication:
    """
    Get the last publication from database using the protrend identifier
    """
    return mapi.get_last_object(Publication, 'protrend_id')
