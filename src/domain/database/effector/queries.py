from typing import List

from data import Effector, Regulator, RegulatoryInteraction, Source
import domain.model_api as mapi
from data.relationships import SourceRelationship


def get_effectors() -> List[Effector]:
    """
    Get effectors list from database
    """
    return mapi.get_objects(Effector)


def filter_effectors(*args, **kwargs) -> List[Effector]:
    """
    Get and filter effectors from database
    """
    return mapi.filter_objects(Effector, *args, **kwargs)


def order_by_effectors(*fields) -> List[Effector]:
    """
    Get and order by effectors from database
    """
    return mapi.order_by_objects(Effector, *fields)


def order_effectors_by_id() -> List[Effector]:
    """
    Get and order by effectors by protrend identifier from database
    """
    return mapi.order_by_objects(Effector, 'protrend_id')


def get_effector(**kwargs) -> Effector:
    """
    Get a given effector from database
    """
    return mapi.get_object(Effector, **kwargs)


def get_effector_by_id(protrend_id: str) -> Effector:
    """
    Get a given effector from database using the protrend identifier
    """
    return mapi.get_object(Effector, protrend_id=protrend_id)


def get_last_effector() -> Effector:
    """
    Get the last effector from database using the protrend identifier
    """
    return mapi.get_last_object(Effector, 'protrend_id')


def get_effector_sources(protrend_id: str) -> List[Source]:
    """
    Get sources connected with this effector
    """
    obj = get_effector_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'data_source')


def get_effector_sources_relationships(protrend_id: str) -> List[SourceRelationship]:
    """
    Get sources relationships connected with this effector
    """
    obj = get_effector_by_id(protrend_id)
    sources = mapi.get_related_objects(obj, 'data_source')
    relationships = []
    for source in sources:
        source_relationships = mapi.get_relationships(source=obj, rel='data_source', target=source)
        relationships.extend(source_relationships)
    return relationships


def get_effector_regulators(protrend_id: str) -> List[Regulator]:
    """
    Get regulators connected with this effector
    """
    obj = get_effector_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'regulator')


def get_effector_interactions(protrend_id: str) -> List[RegulatoryInteraction]:
    """
    Get the last effector from database using the protrend identifier
    """
    obj = get_effector_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'regulatory_interaction')
