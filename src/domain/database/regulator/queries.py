from typing import List

import domain.model_api as mapi
from data import (Gene, RegulatoryInteraction, TFBS, Regulator, Organism, Pathway, Publication, RegulatoryFamily,
                  Effector, Source)
from data.relationships import SourceRelationship


def get_regulators() -> List[Regulator]:
    """
    Get regulators list from database
    """
    return mapi.get_objects(Regulator)


def filter_regulators(*args, **kwargs) -> List[Regulator]:
    """
    Get and filter regulators from database
    """
    return mapi.filter_objects(Regulator, *args, **kwargs)


def order_by_regulators(*fields) -> List[Regulator]:
    """
    Get and order by regulators from database
    """
    return mapi.order_by_objects(Regulator, *fields)


def order_regulators_by_id() -> List[Regulator]:
    """
    Get and order by regulators by protrend identifier from database
    """
    return mapi.order_by_objects(Regulator, 'protrend_id')


def get_regulator(**kwargs) -> Regulator:
    """
    Get a given regulator from database
    """
    return mapi.get_object(Regulator, **kwargs)


def get_regulator_by_id(protrend_id: str) -> Regulator:
    """
    Get a given regulator from database using the protrend identifier
    """
    return mapi.get_object(Regulator, protrend_id=protrend_id)


def get_last_regulator() -> Regulator:
    """
    Get the last regulator from database using the protrend identifier
    """
    return mapi.get_last_object(Regulator, 'protrend_id')


def get_regulator_sources(protrend_id: str) -> List[Source]:
    """
    Get sources connected with this regulator
    """
    obj = get_regulator_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'data_source')


def get_regulator_sources_relationships(protrend_id: str) -> List[SourceRelationship]:
    """
    Get sources relationships connected with this regulator
    """
    obj = get_regulator_by_id(protrend_id)
    sources = mapi.get_related_objects(obj, 'data_source')
    relationships = []
    for source in sources:
        source_relationships = mapi.get_relationships(source_obj=obj, target='data_source', target_obj=source)
        relationships.extend(source_relationships)
    return relationships


def get_regulator_publications(protrend_id: str) -> List[Publication]:
    """
    Get publications connected with this regulator
    """
    obj = get_regulator_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'publication')


def get_regulator_pathways(protrend_id: str) -> List[Pathway]:
    """
    Get pathways connected with this regulator
    """
    obj = get_regulator_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'pathway')


def get_regulator_effectors(protrend_id: str) -> List[Effector]:
    """
    Get effectors connected with this regulator
    """
    obj = get_regulator_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'effector')


def get_regulator_rfams(protrend_id: str) -> List[RegulatoryFamily]:
    """
    Get rfams connected with this regulator
    """
    obj = get_regulator_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'regulatory_family')


def get_regulator_organisms(protrend_id: str) -> List[Organism]:
    """
    Get organism connected with this regulator
    """
    obj = get_regulator_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'organism')


def get_regulator_genes(protrend_id: str) -> List[Gene]:
    """
    Get genes connected with this regulator
    """
    obj = get_regulator_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'gene')


def get_regulator_binding_sites(protrend_id: str) -> List[TFBS]:
    """
    Get binding sites connected with this regulator
    """
    obj = get_regulator_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'tfbs')


def get_regulator_interactions(protrend_id: str) -> List[RegulatoryInteraction]:
    """
    Get interactions connected with this regulator
    """
    obj = get_regulator_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'regulatory_interaction')
