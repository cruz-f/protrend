from typing import List, Dict, Any

from rest_framework import status

from data import RegulatoryInteraction, Organism, Regulator, Gene, TFBS, Effector
import domain.model_api as mapi
from domain.database._validate import _validate_kwargs_by_interaction_hash, _validate_args_by_interaction_hash
from exceptions import ProtrendException


_HEADER = 'PRT'
_ENTITY = 'RIN'


def _validate_submitted_objects(interaction: dict):

    # order matters - do not change dict order
    lookup_queries = {'organism': Organism,
                      'regulator': Regulator,
                      'gene': Gene,
                      'tfbs': TFBS,
                      'effector': Effector}

    objs = []
    for key, model_cls in lookup_queries.items():

        if key in interaction:
            lookup_value = interaction[key]
            obj = mapi.get_object(model_cls, protrend_id=lookup_value)
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
    # organism <-> regulator; gene; tfbs; interaction
    mapi.create_unique_reverse_relationship(source=organism,  forward_rel='regulator',
                                            backward_rel='organism', target=regulator)
    mapi.create_unique_reverse_relationship(source=organism, forward_rel='gene',
                                            backward_rel='organism', target=gene)
    if tfbs is not None:
        mapi.create_unique_reverse_relationship(source=organism, forward_rel='tfbs',
                                                backward_rel='data_organism', target=tfbs)
    mapi.create_unique_reverse_relationship(source=organism, forward_rel='regulatory_interaction',
                                            backward_rel='data_organism', target=interaction)

    # regulator <-> gene; tfbs; effector; interaction
    mapi.create_unique_reverse_relationship(source=regulator, forward_rel='gene',
                                            backward_rel='regulator', target=gene)
    if tfbs is not None:
        mapi.create_unique_reverse_relationship(source=regulator, forward_rel='tfbs',
                                                backward_rel='regulator', target=tfbs)
    if effector is not None:
        mapi.create_unique_reverse_relationship(source=regulator, forward_rel='effector',
                                                backward_rel='regulator', target=effector)
    mapi.create_unique_reverse_relationship(source=regulator, forward_rel='regulatory_interaction',
                                            backward_rel='data_regulator', target=interaction)

    # gene <-> tfbs; interaction
    if tfbs is not None:
        mapi.create_unique_reverse_relationship(source=gene, forward_rel='tfbs',
                                                backward_rel='gene', target=tfbs)
    mapi.create_unique_reverse_relationship(source=gene, forward_rel='regulatory_interaction',
                                            backward_rel='data_gene', target=interaction)

    # tfbs <-> interaction
    if tfbs is not None:
        mapi.create_unique_reverse_relationship(source=tfbs,
                                                forward_rel='regulatory_interaction',
                                                backward_rel='data_tfbs',
                                                target=interaction)

    # effector <-> interaction
    if effector is not None:
        mapi.create_unique_reverse_relationship(source=effector,
                                                forward_rel='regulatory_interaction',
                                                backward_rel='data_effector',
                                                target=interaction)
