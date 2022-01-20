from typing import List

from data import Gene
import domain.model_api as mapi


def get_genes() -> List[Gene]:
    """
    Get genes list from database
    """
    return mapi.get_objects(Gene)


def filter_genes(*args, **kwargs) -> List[Gene]:
    """
    Get and filter genes from database
    """
    return mapi.filter_objects(Gene, *args, **kwargs)


def order_by_genes(*fields) -> List[Gene]:
    """
    Get and order by genes from database
    """
    return mapi.order_by_objects(Gene, *fields)


def order_genes_by_id() -> List[Gene]:
    """
    Get and order by genes by protrend identifier from database
    """
    return mapi.order_by_objects(Gene, 'protrend_id')


def get_gene(**kwargs) -> Gene:
    """
    Get a given gene from database
    """
    return mapi.get_object(Gene, **kwargs)


def get_gene_by_id(protrend_id: str) -> Gene:
    """
    Get a given gene from database using the protrend identifier
    """
    return mapi.get_object(Gene, protrend_id=protrend_id)


def get_last_gene() -> Gene:
    """
    Get the last gene from database using the protrend identifier
    """
    return mapi.get_last_object(Gene, 'protrend_id')
