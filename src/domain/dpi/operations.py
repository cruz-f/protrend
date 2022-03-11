from typing import Union, Type, List, Dict, Any, Callable, Tuple

from django_neomodel import DjangoNode
from neomodel import RelationshipManager, StructuredRel

from data import (Effector,
                  Evidence,
                  Gene,
                  Operon,
                  Organism,
                  Pathway,
                  Publication,
                  Regulator,
                  RegulatoryFamily,
                  RegulatoryInteraction,
                  TFBS, Source)
from .utils import raise_exception
from .validation import (locus_tag_validation,
                         name_validation,
                         uniprot_accession_validation,
                         operon_db_validation,
                         ncbi_taxonomy_validation,
                         pmid_validation,
                         interaction_validation,
                         binding_site_validation)
from domain.neo import NeoNode

_model_type = Union[Type[DjangoNode], Type[NeoNode]]
_model = Union[DjangoNode, NeoNode]


def object_validation(cls: _model_type,
                      values: Tuple,
                      validators: Tuple[Callable] = None):
    if validators:
        return [validator(obj) for obj in values for validator in validators]

    if cls is Effector:
        return name_validation(values=values, node_cls=Effector, header='PRT', entity='EFC')

    elif cls is Evidence:
        return name_validation(values=values, node_cls=Evidence, header='PRT', entity='EVI')

    elif cls is Gene:
        values = locus_tag_validation(values=values, node_cls=Gene, header='PRT', entity='GEN')
        return uniprot_accession_validation(values=values, node_cls=Gene)

    elif cls is Operon:
        return operon_db_validation(values=values, node_cls=Operon, header='PRT', entity='OPN')

    elif cls is Organism:
        values = name_validation(values=values, node_cls=Organism, header='PRT', entity='ORG')
        return ncbi_taxonomy_validation(values=values, node_cls=Organism)

    elif cls is Pathway:
        return name_validation(values=values, node_cls=Pathway, header='PRT', entity='PTH')

    elif cls is Publication:
        return pmid_validation(values=values, node_cls=Publication, header='PRT', entity='PUB')

    elif cls is Regulator:
        values = locus_tag_validation(values=values, node_cls=Regulator, header='PRT', entity='REG')
        return uniprot_accession_validation(values=values, node_cls=Regulator)

    elif cls is RegulatoryFamily:
        return name_validation(values=values, node_cls=RegulatoryFamily, header='PRT', entity='RFAM')

    elif cls is RegulatoryInteraction:
        return interaction_validation(values=values, node_cls=RegulatoryInteraction, header='PRT', entity='RIN')

    elif cls is Source:
        return name_validation(values=values, node_cls=Source, header='PRT', entity='SRC')

    elif cls is TFBS:
        return binding_site_validation(values=values, node_cls=TFBS, header='PRT', entity='TBS')

    return values


# TODO: missing custom interaction and binding site creation and update
# ---------------------------------------------------------
# Bulk Object Create Update and Delete operations
# ---------------------------------------------------------
@raise_exception
def create_objects(cls: _model_type,
                   values: Tuple[Dict[str, Any]],
                   validators: Tuple[Callable] = None) -> List:
    """
    Create multiple objects into the database from a set of dictionaries
    """
    values = object_validation(cls, values, validators)
    return list(cls.create(*values))


@raise_exception
def update_objects(objects: Tuple[_model],
                   values: Tuple[Dict[str, Any]]) -> List:
    """
    Update multiple objects into the database from a set of dictionaries
    """
    for obj, kwargs in zip(objects, values):
        for attr, value in kwargs.items():
            setattr(obj, attr, value)
        obj.save()
    return list(objects)


@raise_exception
def delete_objects(objects: Tuple[_model]):
    """
    Delete multiple objects from the database calling the delete method of these objects
    """
    for obj in objects:
        obj.delete()


# ------------------------------------------------------------------------------
# Relationships - SO FAR THE DOMAIN LAYER ONLY SUPPORTS NEOMODEL RELATIONSHIPS
# ------------------------------------------------------------------------------
def get_rel_query_set(obj: _model, rel: str) -> Union[Any, RelationshipManager]:
    relationship = getattr(obj, rel, None)
    if relationship is not None:
        if hasattr(relationship, 'all'):
            return relationship

    raise AttributeError(f'relationship attribute not found for object {obj.protrend_id}')


# ---------------------------------------------------------
# Relationships Create Read Update and Delete operations
# ---------------------------------------------------------
@raise_exception
def get_relationships(source: _model, rel: str, target: _model):
    """
    Get all relationships objects between two objects
    """
    query_set = get_rel_query_set(obj=source, rel=rel)
    return query_set.all_relationships(target)


@raise_exception
def delete_relationships(source: _model, rel: str, target: _model):
    """
    Delete all relationships between two objects
    """
    query_set = get_rel_query_set(obj=source, rel=rel)
    return query_set.disconnect(target)


@raise_exception
def get_relationship(source: _model, rel: str, target: _model) -> Union[StructuredRel, None]:
    """
    Get the first relationship object between two nodes
    """
    query_set = get_rel_query_set(obj=source, rel=rel)
    return query_set.relationship(target)


@raise_exception
def is_connected(source: _model, rel: str, target: _model) -> bool:
    """
    Get the first relationship object between two nodes
    """
    query_set = get_rel_query_set(obj=source, rel=rel)
    return query_set.is_connected(target)


@raise_exception
def create_relationship(source: _model, rel: str, target: _model, **kwargs) -> Union[StructuredRel, None]:
    """
    Create a relationship object between two objects
    """
    query_set = get_rel_query_set(obj=source, rel=rel)
    return query_set.connect(target, properties=kwargs)


@raise_exception
def create_unique_relationship(source: _model,
                               rel: str,
                               target: _model,
                               **kwargs) -> Union[StructuredRel, None]:
    """
    Create a relationship object between two objects
    """
    query_set = get_rel_query_set(obj=source, rel=rel)

    if not query_set.is_connected(target):
        return query_set.connect(target, properties=kwargs)

    return


@raise_exception
def create_unique_reverse_relationship(source: _model,
                                       forward_rel: str,
                                       backward_rel: str,
                                       target: _model,
                                       **kwargs) -> Tuple[Union[StructuredRel, None], Union[StructuredRel, None]]:
    """
    Create a forward and backward relationship object between two objects if these are not connected
    """
    forward_instance = None
    backward_instance = None

    forward_query_set = get_rel_query_set(obj=source, rel=forward_rel)
    if not forward_query_set.is_connected(target):
        forward_instance = forward_query_set.connect(target, properties=kwargs)

    backward_query_set = get_rel_query_set(obj=target, rel=backward_rel)
    if not backward_query_set.is_connected(source):
        backward_instance = backward_query_set.connect(source, properties=kwargs)

    return forward_instance, backward_instance


@raise_exception
def update_relationship(source: _model, rel: str, target: _model, **kwargs) -> StructuredRel:
    """
    Update a relationship object between two objects
    """
    relationship = get_relationship(source=source, rel=rel, target=target)
    for attr, value in kwargs.items():
        setattr(relationship, attr, value)
    relationship.save()
    return relationship


@raise_exception
def delete_relationship(source: _model, rel: str, target: _model):
    """
    Delete a relationship object between two objects
    """
    return delete_relationships(source=source, rel=rel, target=target)
