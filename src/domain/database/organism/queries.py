import domain.model_api as mapi
from data import Organism
from domain.query import NodeQuerySet


def get_lazy_organisms() -> NodeQuerySet[Organism]:
    """
    Get organisms list from database
    """
    lazy_properties = ['protrend_id', 'name', 'ncbi_taxonomy', 'species', 'strain']
    return mapi.get_lazy_objects(Organism, lazy_properties)


def get_lazy_organisms_query_set() -> NodeQuerySet[Organism]:
    """
    Get organisms query set from database
    """
    lazy_properties = ['protrend_id', 'name', 'ncbi_taxonomy', 'species', 'strain']
    return mapi.get_query_set(Organism, lazy_properties)


def get_lazy_organisms_page() -> NodeQuerySet[Organism]:
    """
    Get organisms list from database
    """
    lazy_properties = ['protrend_id', 'name', 'ncbi_taxonomy', 'species', 'strain',
                       'refseq_accession', 'genbank_accession', 'assembly_accession']
    return mapi.get_lazy_objects(Organism, lazy_properties)