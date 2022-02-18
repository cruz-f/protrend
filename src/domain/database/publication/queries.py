from typing import List

import domain.model_api as mapi
from data import Publication


def get_lazy_publications() -> List[Publication]:
    """
    Get publications identifiers list from database
    """
    lazy_properties = ['protrend_id', 'pmid', 'doi', 'title', 'author', 'year']
    return mapi.get_lazy_objects(Publication, lazy_properties)


def get_lazy_publications_query_set() -> List[Publication]:
    """
    Get publications query set from database
    """
    lazy_properties = ['protrend_id', 'pmid', 'doi', 'title', 'author', 'year']
    return mapi.get_query_set(Publication, lazy_properties)
