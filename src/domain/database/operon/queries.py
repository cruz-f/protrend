import domain.model_api as mapi
from data import Operon
from domain.query import NodeQuerySet


def get_lazy_operons() -> NodeQuerySet[Operon]:
    """
    Get operons list from database
    """
    lazy_properties = ['protrend_id', 'operon_db_id', 'name', 'function', 'genes']
    return mapi.get_lazy_objects(Operon, lazy_properties)


def get_lazy_operons_query_set() -> NodeQuerySet[Operon]:
    """
    Get operons query set from database
    """
    lazy_properties = ['protrend_id', 'operon_db_id', 'name', 'function', 'genes']
    return mapi.get_query_set(Operon, lazy_properties)
