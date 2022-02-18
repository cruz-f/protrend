import domain.model_api as mapi
from data import Gene
from domain.query import NodeQuerySet


def get_lazy_genes() -> NodeQuerySet[Gene]:
    """
    Get genes list from database
    """
    lazy_properties = ['protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'synonyms']
    return mapi.get_lazy_objects(Gene, lazy_properties)


def get_lazy_genes_query_set() -> NodeQuerySet[Gene]:
    """
    Get genes query set from database
    """
    lazy_properties = ['protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'synonyms']
    return mapi.get_query_set(Gene, lazy_properties)
