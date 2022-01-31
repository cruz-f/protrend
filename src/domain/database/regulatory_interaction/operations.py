from typing import List, Dict, Any

from rest_framework import status

from data import RegulatoryInteraction
import domain.model_api as mapi
from domain.database.effector import get_effector_by_id
from domain.database.organism import get_organism_by_id
from domain.database.regulator import get_regulator_by_id
from domain.database.gene import get_gene_by_id
from domain.database.tfbs import get_binding_site_by_id
from domain.database._validate import _validate_kwargs_by_interaction_hash, _validate_args_by_interaction_hash
from exceptions import ProtrendException


_HEADER = 'PRT'
_ENTITY = 'RIN'


lookup_queries = {'organism': get_organism_by_id, 'regulator': get_regulator_by_id,
                  'gene': get_gene_by_id, 'tfbs': get_binding_site_by_id, 'effector': get_effector_by_id}


def _validate_submitted_objects(interaction: dict):
    for key, lookup in lookup_queries.items():

        if key not in interaction:
            continue

        lookup_value = interaction[key]
        obj = lookup(lookup_value)
        if obj is None:
            raise ProtrendException(detail=f'The submitted {lookup_value} protrend id for the property {key} '
                                           f'was not found in the database.',
                                    code='create or update error',
                                    status=status.HTTP_400_BAD_REQUEST)


def create_interactions(*interactions: Dict[str, Any]) -> List[RegulatoryInteraction]:
    """
    Create interactions into the database
    """
    for interaction in interactions:
        _validate_submitted_objects(interaction)

    interactions = _validate_args_by_interaction_hash(args=interactions, node_cls=RegulatoryInteraction,
                                                      header=_HEADER, entity=_ENTITY)
    return mapi.create_objects(RegulatoryInteraction, *interactions)


def delete_interactions(*interactions: RegulatoryInteraction):
    """
    Delete interactions from the database
    """
    return mapi.delete_objects(*interactions)


def create_interaction(**kwargs) -> RegulatoryInteraction:
    """
    Create a given interaction into the database according to the parameters
    """
    _validate_submitted_objects(kwargs)
    kwargs = _validate_kwargs_by_interaction_hash(kwargs=kwargs, node_cls=RegulatoryInteraction,
                                                  header=_HEADER, entity=_ENTITY)
    return mapi.create_object(RegulatoryInteraction, **kwargs)


def update_interaction(interaction: RegulatoryInteraction, **kwargs) -> RegulatoryInteraction:
    """
    Update the interaction into the database according to the parameters
    """
    if 'protrend_id' in kwargs:
        raise ProtrendException(detail=f'protrend_id read-only attribute cannot be altered',
                                code='create or update error',
                                status=status.HTTP_400_BAD_REQUEST)

    _validate_submitted_objects(kwargs)

    # the protrend hash must always be regenerated
    kwargs = _validate_kwargs_by_interaction_hash(kwargs=kwargs, node_cls=RegulatoryInteraction,
                                                  header=_HEADER, entity=_ENTITY)
    kwargs.pop('protrend_id')
    return mapi.update_object(interaction, **kwargs)


def delete_interaction(interaction: RegulatoryInteraction) -> RegulatoryInteraction:
    """
    Delete the interaction from the database
    """
    return mapi.delete_object(interaction)
