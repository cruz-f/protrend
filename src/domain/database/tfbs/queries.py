import domain.model_api as mapi
from data import TFBS
from domain.query import NodeQuerySet


def get_lazy_binding_sites() -> NodeQuerySet[TFBS]:
    """
    Get binding_sites list from database
    """
    lazy_properties = ['protrend_id', 'organism', 'sequence', 'strand', 'start', 'stop', 'length']
    return mapi.get_lazy_objects(TFBS, lazy_properties)


def get_lazy_binding_sites_query_set() -> NodeQuerySet[TFBS]:
    """
    Get binding_sites query set from database
    """
    lazy_properties = ['protrend_id', 'organism', 'sequence', 'strand', 'start', 'stop', 'length']
    return mapi.get_query_set(TFBS, lazy_properties)
