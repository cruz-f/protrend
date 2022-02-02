from typing import List

from data import RegulatoryFamily, Regulator, Source
import domain.model_api as mapi
from data.relationships import SourceRelationship


def get_rfams() -> List[RegulatoryFamily]:
    """
    Get rfams list from database
    """
    return mapi.get_objects(RegulatoryFamily)


def filter_rfams(*args, **kwargs) -> List[RegulatoryFamily]:
    """
    Get and filter rfams from database
    """
    return mapi.filter_objects(RegulatoryFamily, *args, **kwargs)


def order_by_rfams(*fields) -> List[RegulatoryFamily]:
    """
    Get and order by rfams from database
    """
    return mapi.order_by_objects(RegulatoryFamily, *fields)


def order_rfams_by_id() -> List[RegulatoryFamily]:
    """
    Get and order by rfams by protrend identifier from database
    """
    return mapi.order_by_objects(RegulatoryFamily, 'protrend_id')


def get_rfam(**kwargs) -> RegulatoryFamily:
    """
    Get a given rfam from database
    """
    return mapi.get_object(RegulatoryFamily, **kwargs)


def get_rfam_by_id(protrend_id: str) -> RegulatoryFamily:
    """
    Get a given rfam from database using the protrend identifier
    """
    return mapi.get_object(RegulatoryFamily, protrend_id=protrend_id)


def get_last_rfam() -> RegulatoryFamily:
    """
    Get the last rfam from database using the protrend identifier
    """
    return mapi.get_last_object(RegulatoryFamily, 'protrend_id')


def get_rfam_sources(protrend_id: str) -> List[Source]:
    """
    Get sources connected with this rfam
    """
    obj = get_rfam_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'data_source')


def get_rfam_sources_relationships(protrend_id: str) -> List[SourceRelationship]:
    """
    Get sources relationships connected with this rfam
    """
    obj = get_rfam_by_id(protrend_id)
    sources = mapi.get_related_objects(obj, 'data_source')
    relationships = []
    for source in sources:
        source_relationships = mapi.get_relationships(source_obj=obj, target='data_source', target_obj=source)
        relationships.extend(source_relationships)
    return relationships


def get_rfam_regulator(protrend_id: str) -> List[Regulator]:
    """
    Get regulators connected with this rfam
    """
    obj = get_rfam_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'regulator')
