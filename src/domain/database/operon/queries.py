from typing import List

from data import Operon, Organism, Gene, Source
import domain.model_api as mapi
from data.relationships import SourceRelationship


def get_operons() -> List[Operon]:
    """
    Get operons list from database
    """
    return mapi.get_objects(Operon)


def filter_operons(*args, **kwargs) -> List[Operon]:
    """
    Get and filter operons from database
    """
    return mapi.filter_objects(Operon, *args, **kwargs)


def order_by_operons(*fields) -> List[Operon]:
    """
    Get and order by operons from database
    """
    return mapi.order_by_objects(Operon, *fields)


def order_operons_by_id() -> List[Operon]:
    """
    Get and order by operons by protrend identifier from database
    """
    return mapi.order_by_objects(Operon, 'protrend_id')


def get_operon(**kwargs) -> Operon:
    """
    Get a given operon from database
    """
    return mapi.get_object(Operon, **kwargs)


def get_operon_by_id(protrend_id: str) -> Operon:
    """
    Get a given operon from database using the protrend identifier
    """
    return mapi.get_object(Operon, protrend_id=protrend_id)


def get_last_operon() -> Operon:
    """
    Get the last operon from database using the protrend identifier
    """
    return mapi.get_last_object(Operon, 'protrend_id')


def get_operon_sources(protrend_id: str) -> List[Source]:
    """
    Get sources connected with this operon
    """
    obj = get_operon_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'data_source')


def get_operon_sources_relationships(protrend_id: str) -> List[SourceRelationship]:
    """
    Get sources relationships connected with this operon
    """
    obj = get_operon_by_id(protrend_id)
    sources = mapi.get_related_objects(obj, 'data_source')
    relationships = []
    for source in sources:
        source_relationships = mapi.get_relationships(source=obj, rel='data_source', target=source)
        relationships.extend(source_relationships)
    return relationships


def get_operon_organisms(protrend_id: str) -> List[Organism]:
    """
    Get organism connected with this operon
    """
    obj = get_operon_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'organism')


def get_operon_genes(protrend_id: str) -> List[Gene]:
    """
    Get genes connected with this operon
    """
    obj = get_operon_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'gene')
