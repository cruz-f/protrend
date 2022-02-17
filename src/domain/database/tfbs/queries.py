from typing import List

import domain.model_api as mapi
from data import TFBS


def get_lazy_binding_sites() -> List[TFBS]:
    """
    Get binding_sites list from database
    """
    lazy_properties = ['protrend_id', 'organism', 'sequence', 'strand', 'start', 'stop', 'length']
    return mapi.get_lazy_objects(TFBS, lazy_properties)