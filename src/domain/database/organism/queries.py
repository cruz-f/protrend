from typing import List

from data import Organism, Gene, TFBS, RegulatoryInteraction, Regulator, Source
import domain.model_api as mapi
from data.relationships import SourceRelationship


def get_organisms() -> List[Organism]:
    """
    Get organisms list from database
    """
    return mapi.get_objects(Organism)


def filter_organisms(*args, **kwargs) -> List[Organism]:
    """
    Get and filter organisms from database
    """
    return mapi.filter_objects(Organism, *args, **kwargs)


def order_by_organisms(*fields) -> List[Organism]:
    """
    Get and order by organisms from database
    """
    return mapi.order_by_objects(Organism, *fields)


def order_organisms_by_id() -> List[Organism]:
    """
    Get and order by organisms by protrend identifier from database
    """
    return mapi.order_by_objects(Organism, 'protrend_id')


def get_organism(**kwargs) -> Organism:
    """
    Get a given organism from database
    """
    return mapi.get_object(Organism, **kwargs)


def get_organism_by_id(protrend_id: str) -> Organism:
    """
    Get a given organism from database using the protrend identifier
    """
    return mapi.get_object(Organism, protrend_id=protrend_id)


def get_last_organism() -> Organism:
    """
    Get the last organism from database using the protrend identifier
    """
    return mapi.get_last_object(Organism, 'protrend_id')


def get_organism_sources(protrend_id: str) -> List[Source]:
    """
    Get sources connected with this organism
    """
    obj = get_organism_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'data_source')


def get_organism_sources_relationships(protrend_id: str) -> List[SourceRelationship]:
    """
    Get sources relationships connected with this organism
    """
    obj = get_organism_by_id(protrend_id)
    sources = mapi.get_related_objects(obj, 'data_source')
    relationships = []
    for source in sources:
        source_relationships = mapi.get_relationships(source_obj=obj, target='data_source', target_obj=source)
        relationships.extend(source_relationships)
    return relationships


def get_organism_regulators(protrend_id: str) -> List[Regulator]:
    """
    Get regulators connected with this organism
    """
    obj = get_organism_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'regulator')


def get_organism_genes(protrend_id: str) -> List[Gene]:
    """
    Get genes connected with this organism
    """
    obj = get_organism_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'gene')


def get_organism_binding_sites(protrend_id: str) -> List[TFBS]:
    """
    Get binding sites connected with this organism
    """
    obj = get_organism_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'tfbs')


def get_organism_interactions(protrend_id: str) -> List[RegulatoryInteraction]:
    """
    Get interactions connected with this organism
    """
    obj = get_organism_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'regulatory_interaction')
