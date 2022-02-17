from typing import List

import domain.model_api as mapi
from data import Gene


def get_lazy_genes() -> List[Gene]:
    """
    Get genes list from database
    """
    lazy_properties = ['protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'synonyms']
    return mapi.get_lazy_objects(Gene, lazy_properties)
