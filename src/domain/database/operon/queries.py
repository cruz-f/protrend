from typing import List

import domain.model_api as mapi
from data import Operon


def get_lazy_operons() -> List[Operon]:
    """
    Get operons list from database
    """
    lazy_properties = ['protrend_id', 'operon_db_id', 'name', 'function', 'genes']
    return mapi.get_lazy_objects(Operon, lazy_properties)
