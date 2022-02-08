from typing import List

from data import TFBS, Evidence, Publication, Organism, Regulator, Gene, RegulatoryInteraction, Source
import domain.model_api as mapi
from data.relationships import SourceRelationship


def get_binding_sites() -> List[TFBS]:
    """
    Get binding_sites list from database
    """
    return mapi.get_objects(TFBS)


def filter_binding_sites(*args, **kwargs) -> List[TFBS]:
    """
    Get and filter binding_sites from database
    """
    return mapi.filter_objects(TFBS, *args, **kwargs)


def order_by_binding_sites(*fields) -> List[TFBS]:
    """
    Get and order by binding_sites from database
    """
    return mapi.order_by_objects(TFBS, *fields)


def order_binding_sites_by_id() -> List[TFBS]:
    """
    Get and order by binding_sites by protrend identifier from database
    """
    return mapi.order_by_objects(TFBS, 'protrend_id')


def get_binding_site(**kwargs) -> TFBS:
    """
    Get a given binding_site from database
    """
    return mapi.get_object(TFBS, **kwargs)


def get_binding_site_by_id(protrend_id: str) -> TFBS:
    """
    Get a given binding_site from database using the protrend identifier
    """
    return mapi.get_object(TFBS, protrend_id=protrend_id)


def get_last_binding_site() -> TFBS:
    """
    Get the last binding_site from database using the protrend identifier
    """
    return mapi.get_last_object(TFBS, 'protrend_id')


def get_binding_site_sources(protrend_id: str) -> List[Source]:
    """
    Get sources connected with this binding_site
    """
    obj = get_binding_site_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'data_source')


def get_binding_site_sources_relationships(protrend_id: str) -> List[SourceRelationship]:
    """
    Get sources relationships connected with this binding_site
    """
    obj = get_binding_site_by_id(protrend_id)
    sources = mapi.get_related_objects(obj, 'data_source')
    relationships = []
    for source in sources:
        source_relationships = mapi.get_relationships(source=obj, rel='data_source', target=source)
        relationships.extend(source_relationships)
    return relationships


def get_binding_site_evidences(protrend_id: str) -> List[Evidence]:
    """
    Get evidences connected with this binding_site
    """
    obj = get_binding_site_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'evidence')


def get_binding_site_publications(protrend_id: str) -> List[Publication]:
    """
    Get publications connected with this binding_site
    """
    obj = get_binding_site_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'publication')


def get_binding_site_organisms(protrend_id: str) -> List[Organism]:
    """
    Get organism connected with this binding_site
    """
    obj = get_binding_site_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'data_organism')


def get_binding_site_regulators(protrend_id: str) -> List[Regulator]:
    """
    Get regulators connected with this binding_site
    """
    obj = get_binding_site_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'regulator')


def get_binding_site_genes(protrend_id: str) -> List[Gene]:
    """
    Get genes connected with this binding_site
    """
    obj = get_binding_site_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'gene')


def get_binding_site_interactions(protrend_id: str) -> List[RegulatoryInteraction]:
    """
    Get interactions connected with this binding_site
    """
    obj = get_binding_site_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'regulatory_interaction')
