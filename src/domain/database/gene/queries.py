from typing import List

from data import Gene, RegulatoryInteraction, TFBS, Regulator, Organism, Operon, Pathway, Publication, Source
import domain.model_api as mapi
from data.relationships import SourceRelationship


def get_genes() -> List[Gene]:
    """
    Get genes list from database
    """
    return mapi.get_objects(Gene)


def filter_genes(*args, **kwargs) -> List[Gene]:
    """
    Get and filter genes from database
    """
    return mapi.filter_objects(Gene, *args, **kwargs)


def order_by_genes(*fields) -> List[Gene]:
    """
    Get and order by genes from database
    """
    return mapi.order_by_objects(Gene, *fields)


def order_genes_by_id() -> List[Gene]:
    """
    Get and order by genes by protrend identifier from database
    """
    return mapi.order_by_objects(Gene, 'protrend_id')


def get_gene(**kwargs) -> Gene:
    """
    Get a given gene from database
    """
    return mapi.get_object(Gene, **kwargs)


def get_gene_by_id(protrend_id: str) -> Gene:
    """
    Get a given gene from database using the protrend identifier
    """
    return mapi.get_object(Gene, protrend_id=protrend_id)


def get_last_gene() -> Gene:
    """
    Get the last gene from database using the protrend identifier
    """
    return mapi.get_last_object(Gene, 'protrend_id')


def get_effector_sources(protrend_id: str) -> List[Source]:
    """
    Get sources connected with this gene
    """
    obj = get_gene_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'data_source')


def get_gene_sources_relationships(protrend_id: str) -> List[SourceRelationship]:
    """
    Get sources relationships connected with this gene
    """
    obj = get_gene_by_id(protrend_id)
    sources = mapi.get_related_objects(obj, 'data_source')
    relationships = []
    for source in sources:
        source_relationships = mapi.get_relationships(source_obj=obj, target='data_source', target_obj=source)
        relationships.extend(source_relationships)
    return relationships


def get_gene_publications(protrend_id: str) -> List[Publication]:
    """
    Get publications connected with this gene
    """
    obj = get_gene_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'publication')


def get_gene_pathways(protrend_id: str) -> List[Pathway]:
    """
    Get pathways connected with this gene
    """
    obj = get_gene_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'pathway')


def get_gene_operons(protrend_id: str) -> List[Operon]:
    """
    Get operons connected with this gene
    """
    obj = get_gene_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'operon')


def get_gene_organisms(protrend_id: str) -> List[Organism]:
    """
    Get organism connected with this gene
    """
    obj = get_gene_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'organism')


def get_gene_regulators(protrend_id: str) -> List[Regulator]:
    """
    Get regulator connected with this gene
    """
    obj = get_gene_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'regulator')


def get_gene_binding_sites(protrend_id: str) -> List[TFBS]:
    """
    Get binding sites connected with this gene
    """
    obj = get_gene_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'tfbs')


def get_gene_interactions(protrend_id: str) -> List[RegulatoryInteraction]:
    """
    Get interactions connected with this gene
    """
    obj = get_gene_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'regulatory_interaction')
