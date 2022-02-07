from typing import List, Dict, Any

from rest_framework import status

from data import RegulatoryInteraction, Organism, Regulator, Gene, TFBS, Effector
import domain.model_api as mapi
from domain.database._validate import _validate_kwargs_by_interaction_hash, _validate_args_by_interaction_hash
from exceptions import ProtrendException


_HEADER = 'PRT'
_ENTITY = 'RIN'


def _validate_submitted_objects(interaction: dict):
    from domain.database.effector.queries import get_effector_by_id
    from domain.database.organism.queries import get_organism_by_id
    from domain.database.regulator.queries import get_regulator_by_id
    from domain.database.gene.queries import get_gene_by_id
    from domain.database.tfbs.queries import get_binding_site_by_id

    # order matters - do not change dict order
    lookup_queries = {'organism': get_organism_by_id,
                      'regulator': get_regulator_by_id,
                      'gene': get_gene_by_id,
                      'tfbs': get_binding_site_by_id,
                      'effector': get_effector_by_id}

    objs = []
    for key, lookup in lookup_queries.items():

        if key in interaction:
            lookup_value = interaction[key]
            obj = lookup(lookup_value)
            if obj is None:
                raise ProtrendException(detail=f'The submitted {lookup_value} protrend id for the property {key} '
                                               f'was not found in the database.',
                                        code='create or update error',
                                        status=status.HTTP_400_BAD_REQUEST)

            objs.append(obj)

        else:
            objs.append(None)

    return objs


def create_interactions(*interactions: Dict[str, Any]) -> List[RegulatoryInteraction]:
    """
    Create interactions into the database
    """
    submitted_objs = []
    for interaction in interactions:
        submitted_obj = _validate_submitted_objects(interaction)
        submitted_objs.append(submitted_obj)

    interactions = _validate_args_by_interaction_hash(args=interactions, node_cls=RegulatoryInteraction,
                                                      header=_HEADER, entity=_ENTITY)

    objs = mapi.create_objects(RegulatoryInteraction, *interactions)

    for obj, submitted_obj in zip(objs, submitted_objs):
        organism, regulator, gene, tfbs, effector = submitted_obj
        try:
            create_interaction_relationships(interaction=obj,
                                             organism=organism, regulator=regulator, gene=gene, tfbs=tfbs,
                                             effector=effector)

        except ProtrendException:
            # if something goes wrong the interaction must be deleted
            delete_interaction(obj)

    return objs


def delete_interactions(*interactions: RegulatoryInteraction):
    """
    Delete interactions from the database
    """
    return mapi.delete_objects(*interactions)


def create_interaction(**kwargs) -> RegulatoryInteraction:
    """
    Create a given interaction into the database according to the parameters
    """
    organism, regulator, gene, tfbs, effector = _validate_submitted_objects(kwargs)
    kwargs = _validate_kwargs_by_interaction_hash(kwargs=kwargs, node_cls=RegulatoryInteraction,
                                                  header=_HEADER, entity=_ENTITY)
    obj = mapi.create_object(RegulatoryInteraction, **kwargs)
    try:
        create_interaction_relationships(interaction=obj,
                                         organism=organism, regulator=regulator,
                                         gene=gene, tfbs=tfbs, effector=effector)

    except ProtrendException:
        # if something happens the interaction must be deleted
        delete_interaction(obj)

    return obj


def update_interaction(_: RegulatoryInteraction, **kwargs) -> RegulatoryInteraction:
    """
    Update the interaction into the database according to the parameters
    """
    raise ProtrendException(detail=f'RegulatoryInteraction update operation is not supported. '
                                   f'Please create a new interaction',
                            code='create or update error',
                            status=status.HTTP_400_BAD_REQUEST)


def delete_interaction(interaction: RegulatoryInteraction) -> RegulatoryInteraction:
    """
    Delete the interaction from the database
    """
    return mapi.delete_object(interaction)


def create_interaction_relationships(interaction: RegulatoryInteraction,
                                     organism: Organism,
                                     regulator: Regulator,
                                     gene: Gene,
                                     tfbs: TFBS,
                                     effector: Effector):
    """
    Create a relationship between interactions and organism regulator gene tfbs effector
    """
    # organism → regulator; gene; interaction
    mapi.create_or_none(source_obj=organism, target='regulator', target_obj=regulator)
    mapi.create_or_none(source_obj=organism, target='gene', target_obj=gene)
    mapi.create_or_none(source_obj=organism, target='regulatory_interaction', target_obj=interaction)

    # regulator → organism; gene; tfbs; effector; interaction
    mapi.create_or_none(source_obj=regulator, target='organism', target_obj=organism)
    mapi.create_or_none(source_obj=regulator, target='gene', target_obj=gene)
    if tfbs is not None:
        mapi.create_or_none(source_obj=regulator, target='tfbs', target_obj=tfbs)
    if effector is not None:
        mapi.create_or_none(source_obj=regulator, target='effector', target_obj=effector)
    mapi.create_or_none(source_obj=regulator, target='regulatory_interaction', target_obj=interaction)

    # gene → organism; regulator; tfbs; interaction
    mapi.create_or_none(source_obj=gene, target='organism', target_obj=organism)
    mapi.create_or_none(source_obj=gene, target='regulator', target_obj=regulator)
    if tfbs is not None:
        mapi.create_or_none(source_obj=gene, target='tfbs', target_obj=tfbs)
    mapi.create_or_none(source_obj=gene, target='regulatory_interaction', target_obj=interaction)

    # tfbs → regulator; gene; interaction
    if tfbs is not None:
        mapi.create_or_none(source_obj=tfbs, target='regulator', target_obj=regulator)
        mapi.create_or_none(source_obj=tfbs, target='gene', target_obj=gene)
        mapi.create_or_none(source_obj=tfbs, target='regulatory_interaction', target_obj=interaction)

    # effector → regulator; interaction
    if effector is not None:
        mapi.create_or_none(source_obj=effector, target='regulator', target_obj=regulator)
        mapi.create_or_none(source_obj=effector, target='regulatory_interaction', target_obj=interaction)

    # interaction → organism; regulator; gene; tfbs; effector
    mapi.create_or_none(source_obj=interaction, target='data_organism', target_obj=organism)
    mapi.create_or_none(source_obj=interaction, target='data_regulator', target_obj=regulator)
    mapi.create_or_none(source_obj=interaction, target='data_gene', target_obj=gene)
    if tfbs is not None:
        mapi.create_or_none(source_obj=interaction, target='data_tfbs', target_obj=tfbs)
    if effector is not None:
        mapi.create_or_none(source_obj=interaction, target='data_effector', target_obj=effector)
