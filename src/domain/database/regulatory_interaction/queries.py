import domain.model_api as mapi
from data import RegulatoryInteraction
from domain.query import NodeQuerySet


def get_lazy_interactions() -> NodeQuerySet[RegulatoryInteraction]:
    """
    Get interactions list from database
    """
    lazy_properties = ['protrend_id', 'organism', 'regulator', 'gene', 'tfbs', 'effector', 'regulatory_effect']
    return mapi.get_lazy_objects(RegulatoryInteraction, lazy_properties)


def get_lazy_interactions_query_set() -> NodeQuerySet[RegulatoryInteraction]:
    """
    Get interactions query set from database
    """
    lazy_properties = ['protrend_id', 'organism', 'regulator', 'gene', 'tfbs', 'effector', 'regulatory_effect']
    return mapi.get_query_set(RegulatoryInteraction, lazy_properties)
