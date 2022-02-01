from typing import List

from data import RegulatoryInteraction, Evidence, Publication, Effector, Organism, Gene, TFBS, Regulator, Source
import domain.model_api as mapi
from data.relationships import SourceRelationship


def get_interactions() -> List[RegulatoryInteraction]:
    """
    Get interactions list from database
    """
    return mapi.get_objects(RegulatoryInteraction)


def filter_interactions(*args, **kwargs) -> List[RegulatoryInteraction]:
    """
    Get and filter interactions from database
    """
    return mapi.filter_objects(RegulatoryInteraction, *args, **kwargs)


def order_by_interactions(*fields) -> List[RegulatoryInteraction]:
    """
    Get and order by interactions from database
    """
    return mapi.order_by_objects(RegulatoryInteraction, *fields)


def order_interactions_by_id() -> List[RegulatoryInteraction]:
    """
    Get and order by interactions by protrend identifier from database
    """
    return mapi.order_by_objects(RegulatoryInteraction, 'protrend_id')


def get_interaction(**kwargs) -> RegulatoryInteraction:
    """
    Get a given interaction from database
    """
    return mapi.get_object(RegulatoryInteraction, **kwargs)


def get_interaction_by_id(protrend_id: str) -> RegulatoryInteraction:
    """
    Get a given interaction from database using the protrend identifier
    """
    return mapi.get_object(RegulatoryInteraction, protrend_id=protrend_id)


def get_last_interaction() -> RegulatoryInteraction:
    """
    Get the last interaction from database using the protrend identifier
    """
    return mapi.get_last_object(RegulatoryInteraction, 'protrend_id')


def get_interaction_sources(protrend_id: str) -> List[Source]:
    """
    Get sources connected with this interaction
    """
    obj = get_interaction_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'data_source')


def get_interaction_sources_relationships(protrend_id: str) -> List[SourceRelationship]:
    """
    Get sources relationships connected with this interaction
    """
    obj = get_interaction_by_id(protrend_id)
    sources = mapi.get_related_objects(obj, 'data_source')
    relationships = []
    for source in sources:
        source_relationships = mapi.get_relationships(source_obj=obj, target='data_source', target_obj=source)
        relationships.extend(source_relationships)
    return relationships


def get_interaction_evidences(protrend_id: str) -> List[Evidence]:
    """
    Get evidences connected with this interaction
    """
    obj = get_interaction_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'evidence')


def get_interaction_publications(protrend_id: str) -> List[Publication]:
    """
    Get publications connected with this interaction
    """
    obj = get_interaction_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'publication')


def get_interaction_effectors(protrend_id: str) -> List[Effector]:
    """
    Get effector connected with this interaction
    """
    obj = get_interaction_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'data_effector')


def get_interaction_organisms(protrend_id: str) -> List[Organism]:
    """
    Get organism connected with this interaction
    """
    obj = get_interaction_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'data_organism')


def get_interaction_regulators(protrend_id: str) -> List[Regulator]:
    """
    Get regulator connected with this interaction
    """
    obj = get_interaction_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'data_regulator')


def get_interaction_genes(protrend_id: str) -> List[Gene]:
    """
    Get gene connected with this interaction
    """
    obj = get_interaction_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'data_gene')


def get_interaction_binding_sites(protrend_id: str) -> List[TFBS]:
    """
    Get binding sites connected with this interaction
    """
    obj = get_interaction_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'data_tfbs')
