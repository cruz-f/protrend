from typing import List

import domain.model_api as mapi
from data import Regulator


def get_lazy_regulators() -> List[Regulator]:
    """
    Get regulators list from database
    """
    lazy_properties = ['protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'synonyms', 'mechanism']
    return mapi.get_lazy_objects(Regulator, lazy_properties)
