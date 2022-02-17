from typing import List

import domain.model_api as mapi
from data import Organism


def get_lazy_organisms() -> List[Organism]:
    """
    Get organisms list from database
    """
    lazy_properties = ['protrend_id', 'name', 'ncbi_taxonomy', 'species', 'strain']
    return mapi.get_lazy_objects(Organism, lazy_properties)
