from typing import List

import domain.model_api as mapi
from data import RegulatoryInteraction


def get_lazy_interactions() -> List[RegulatoryInteraction]:
    """
    Get interactions list from database
    """
    lazy_properties = ['protrend_id', 'organism', 'regulator', 'gene', 'tfbs', 'effector', 'regulatory_effect']
    return mapi.get_lazy_objects(RegulatoryInteraction, lazy_properties)
